import struct
from numbers import Real
from typing import Optional

# Major and minor version of required firmware
_REQUIRED_FIRMWARE_VERSION = (1, 0)


class FirmwareVersionMismatch(Exception):
    pass


class WhoAmIMismatch(Exception):
    pass


class Controller:

    I2C_ADDR = 0x57

    CMD_FIRMWARE_VERSION = 0x08
    CMD_WHO_AM_I = 0x0F
    CMD_PWM_FREQUENCY = 0x10
    CMD_PID_K_P = 0x20
    CMD_PID_K_I = 0x21
    CMD_PID_K_D = 0x22
    CMD_MOTOR_SHUTDOWN_TIMEOUT = 0x28
    CMD_RAW_MOTOR_SPEED = 0x30
    CMD_CONTROLLED_MOTOR_SPEED = 0x31
    CMD_ENCODER_TICKS = 0x32
    CMD_STATUS = 0x36
    CMD_RESET = 0xE0
    CMD_REBOOT_TO_BOOTLOADER = 0xE1
    CMD_DEVICE_ID = 0xF0
    CMD_DEVICE_FAMILY = 0xF1
    CMD_MCU_IDCODE = 0xF2
    CMD_FLASH_SIZE = 0xF3
    CMD_FIRMWARE_CAPABILITIES = 0xFE

    PID_COEFFICIENTS_FACTOR = 1 << 8

    def __init__(self, i2c_bus=8):
        import smbus

        self.i2c_bus = i2c_bus
        self.i2c = smbus.SMBus(self.i2c_bus)

        self.check_who_am_i()
        self.check_firmware_version()

    def _read(self, command, n, unpack_spec) -> tuple:
        return struct.unpack(
            unpack_spec,
            bytes(self.i2c.read_i2c_block_data(self.I2C_ADDR, command, n)),
        )

    def _write(self, command: int, data: list[int]):
        self.i2c.write_i2c_block_data(self.I2C_ADDR, command, data)

    def who_am_i(self) -> int:
        """Check that the motors controller board is present. This
        should return the same value as Controller.I2C_ADDR."""
        return self._read(self.CMD_WHO_AM_I, 1, "B")[0]

    def check_who_am_i(self):
        """Check that the device answers to WHO_AM_I is correct."""
        w = self.who_am_i()
        if w != self.I2C_ADDR:
            error = (
                f"WHO_AM_I returns {w:#04x} "
                f"instead of the expected {self.I2C_ADDR:#04x}"
            )
            raise WhoAmIMismatch(error)

    def set_raw_motor_speed(self, left: Optional[float], right: Optional[float]):
        """Set the motor speed between -127 and 127. None means not to
        change the motor value. Using None for both motors will put
        the controller board in standby mode and motors will stop.

        The speed set through this method will not be regulated by
        the builtin PID controller."""

        def convert(v: Optional[float], arg: str):
            if v is None:
                return -128
            if not isinstance(v, Real) or v < -127 or v > 127:
                raise ValueError(
                    f"{arg} motor speed "
                    "must be a number between -127 and 127, or None"
                )
            return round(v)

        self._write(
            self.CMD_RAW_MOTOR_SPEED,
            list(struct.pack("bb", convert(left, "left"), convert(right, "right"))),
        )

    def get_raw_motor_speed(self) -> Optional[tuple[int, int]]:
        """Get the left and right motor speed as a tuple, or None if in standby.
        Each speed will be between -127 and 127."""
        (left, right) = self._read(self.CMD_RAW_MOTOR_SPEED, 2, "bb")
        return (left, right) if left != -128 and right != -128 else None

    def set_motor_speed(self, left: int, right: int):
        """Set the motor speed in ticks by 100th of seconds. Each motor speed
        must be comprised between -32767 and 32767."""

        def check(v: int, arg: str):
            if v < -32767 or v > 32767:
                raise ValueError(
                    f"{arg} motor speed must be a number " + "between -32767 and 32767"
                )
            return v

        self._write(
            self.CMD_CONTROLLED_MOTOR_SPEED,
            list(struct.pack("<hh", check(left, "left"), check(right, "right"))),
        )

    def get_motor_speed(self):
        """Get the left and right motor speed as a tuple, or None if
        the speed has been set by the raw mode method or if the
        motors have been put into standby mode. The speed is in
        ticks by 100th of seconds."""
        (left, right) = self._read(self.CMD_CONTROLLED_MOTOR_SPEED, 4, "<hh")
        return (left, right) if left != -32768 else None

    def standby(self):
        """Stop the motors by putting the controller board in standby
        mode."""
        self.set_raw_motor_speed(None, None)

    def get_encoder_ticks(self) -> tuple[int, int]:
        """Retrieve the encoder ticks since the last time it was
        queried. The ticks must be retrieved before they overflow a 2
        byte signed integer (-32768..32767) or the result will make no
        sense. Return a pair with left and right data."""
        return self._read(self.CMD_ENCODER_TICKS, 4, "hh")

    def get_status(self) -> dict[str, bool]:
        """Return a dict with status fields:
        - "moving": True if at least one motor is moving, False otherwise
        - "controlled": True if the motors are in controlled mode, False otherwise"""
        (status,) = self._read(self.CMD_STATUS, 1, "B")
        return {"moving": (status & 1) != 0, "controlled": (status & 2) != 0}

    def set_motor_shutdown_timeout(self, duration: float):
        """Set the duration in seconds after which the motors will
        shut down if no valid command is received. The minimum is 0.1
        seconds, the maximum is 10 seconds."""
        if duration < 0.1 or duration > 10.0:
            raise ValueError
        self._write(self.CMD_MOTOR_SHUTDOWN_TIMEOUT, [round(duration * 10)])

    def get_motor_shutdown_timeout(self) -> float:
        """Get the duration in seconds after which the motors will shut down
        if no valid command is received."""
        return self._read(self.CMD_MOTOR_SHUTDOWN_TIMEOUT, 1, "B")[0] / 10

    def get_firmware_version(self) -> tuple[int, int, int]:
        """Get the firmware version (major, minor, patch)."""
        return self._read(self.CMD_FIRMWARE_VERSION, 3, "BBB")

    def check_firmware_version(self):
        """Check that the firmware uses a version compatible with this
        library."""
        version = self.get_firmware_version()
        Controller._check_firmware_version_consistency(
            _REQUIRED_FIRMWARE_VERSION, version
        )

    def _check_firmware_version_consistency(
        required: tuple[int, int], version: tuple[int, int, int]
    ):
        (MAJOR, MINOR) = required
        (major, minor, patch) = version
        error = None
        if major != MAJOR or minor < MINOR:
            version = f"{major}.{minor}.{patch}"
            VERSION = f"{MAJOR}.{MINOR}.*"
            error = (
                f"Hardware runs firmware version {version} which "
                f"is not compatible with this library version ({VERSION})"
            )
            raise FirmwareVersionMismatch(error)

    def set_pwm_frequency(self, freq: int):
        """Set the PWM frequency in Hz, between 1 and 100000."""
        if freq < 1 or freq > 100000:
            raise ValueError(f"PWM frequency is out of [1, 100000] range: {freq}")
        self._write(
            self.CMD_PWM_FREQUENCY,
            [freq & 0xFF, (freq >> 8) & 0xFF, (freq >> 16) & 0xFF],
        )

    def get_pwm_frequency(self):
        """Return the PWM frequency in Hz."""
        a, b, c = self._read(self.CMD_PWM_FREQUENCY, 3, "BBB")
        return a | (b << 8) | (c << 16)

    def reset(self):
        """Reset the device. Used mainly for testing."""
        self._write(self.CMD_RESET, [])

    def reset_to_bootloader(self):
        """Reset the device to bootloader mode. Used for reprogramming."""
        self._write(self.CMD_REBOOT_TO_BOOTLOADER, [])

    def get_device_id(self):
        """Return the 8 bytes composing the device id."""
        return list(self._read(self.CMD_DEVICE_ID, 8, "BBBBBBBB"))

    def get_firmware_capabilities(self) -> dict[str, bool]:
        """Return a dict with capabilities fields:
        - "bootloader": True if the firmware runs under a bootloader, False otherwise.
        """
        (capabilities,) = self._read(self.CMD_FIRMWARE_CAPABILITIES, 1, "B")
        return {"bootloader": (capabilities & 1) != 0}

    def set_pid_coefficients(self, k_p: float, k_i: float, k_d: float):
        """Set the PID coefficients used in the controlled mode. The precision
        is limited to 2^-PID_COEFFICIENTS_FACTOR, and values will be rounded
        as necessary."""

        def convert(v):
            return round(v * self.PID_COEFFICIENTS_FACTOR)

        self._write(self.CMD_PID_K_P, list(struct.pack("<i", convert(k_p))))
        self._write(self.CMD_PID_K_I, list(struct.pack("<i", convert(k_i))))
        self._write(self.CMD_PID_K_D, list(struct.pack("<i", convert(k_d))))

    def get_pid_coefficients(self) -> tuple[float, float, float]:
        """Get the PID coefficients used in the controlled mode."""

        def convert(v):
            return v / self.PID_COEFFICIENTS_FACTOR

        (k_p,) = self._read(self.CMD_PID_K_P, 4, "<i")
        (k_i,) = self._read(self.CMD_PID_K_I, 4, "<i")
        (k_d,) = self._read(self.CMD_PID_K_D, 4, "<i")
        return (convert(k_p), convert(k_i), convert(k_d))

    def get_device_family(self) -> Optional[tuple[int, int]]:
        """Return the microcontroller identity and continuation code
        if they are read succesfully."""
        (id_code, continuation_code) = self._read(self.CMD_DEVICE_FAMILY, 2, "<BB")
        return (
            (id_code, continuation_code)
            if id_code != 0 or continuation_code != 0
            else None
        )

    def get_mcu_kind(self) -> tuple[int, int]:
        """Return the device id and revision id from the IDCODE field
        of the DBGMCU register if they are read succesfully."""
        (dev_id, rev_id) = self._read(self.CMD_MCU_IDCODE, 4, "<HH")
        return (dev_id, rev_id) if dev_id != 0 or rev_id != 0 else None

    def get_flash_size(self) -> int:
        """Return the flash size in kiB as declared by the microcontroller."""
        (flash_size,) = self._read(self.CMD_FLASH_SIZE, 2, "<H")
        return flash_size

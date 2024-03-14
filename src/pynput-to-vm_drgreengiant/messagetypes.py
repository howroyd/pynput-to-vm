import collections.abc
import dataclasses
import enum
import importlib.metadata

#import pynput
import pynput.keyboard as pykeyboard
import pynput.mouse as pymouse
import semantic_version

VERSION = semantic_version.Version.coerce(importlib.metadata.version("pynput-to-vm-drgreengiant"))


@enum.unique
class DeviceType(enum.Enum):
    KEYBOARD = 1
    MOUSE_MOVE = 2
    MOUSE_BUTTON = 3


@dataclasses.dataclass(frozen=True, slots=True)
class Header(collections.abc):
    version: semantic_version.Version
    device_type: DeviceType


def make_header(device_type: DeviceType, *, version: semantic_version = None) -> Header:
    return Header(version or VERSION, device_type)


@dataclasses.dataclass(frozen=True, slots=True)
class EventBase(collections.abc):
    ts: float


@dataclasses.dataclass(frozen=True, slots=True)
class KeyboardEvent(EventBase):
    key: pykeyboard.Key
    pressed: bool


@dataclasses.dataclass(frozen=True, slots=True)
class MouseMoveEvent(EventBase):
    x: int
    y: int


@dataclasses.dataclass(frozen=True, slots=True)
class MouseButtonEvent(EventBase):
    button: pymouse.Button
    pressed: bool


@dataclasses.dataclass(frozen=True, slots=True)
class Message:
    header: Header
    message: EventBase

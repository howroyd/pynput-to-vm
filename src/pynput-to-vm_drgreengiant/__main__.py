from . import messagetypes as msgtypes

if __name__ == "__main__":
    hdr = msgtypes.make_header(msgtypes.DeviceType.KEYBOARD)

    print(hdr)
    print(hdr.asdict())

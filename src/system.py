import ctypes
import platform


def is_windows():
    # True if windows, false otherwise
    return platform.system() == "Windows"


def get_dpi_scaling_factor():
    # Default scaling factor
    dpi_scaling = 1.0

    # Platform is windows
    if is_windows():
        try:
            # This will set the DPI awareness to per-monitor (for Windows 10 and below)
            ctypes.windll.user32.SetProcessDPIAware()

            # Leave scaling factor as-is

        except AttributeError:
            # Get the primary monitor's DPI (96 is default at 100% scaling)
            hdc = ctypes.windll.user32.GetDC(0)
            dpi_x = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)
            dpi_scaling = dpi_x / 96  # Default DPI is 96, so scaling is dpi_x / 96
            ctypes.windll.user32.ReleaseDC(0, hdc)

    # Otherwise, leave as-is

    return dpi_scaling

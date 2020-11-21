import threading
import time
from _winapi import GENERIC_READ, OPEN_EXISTING, GENERIC_WRITE
from ctypes import Structure, byref, sizeof, POINTER, windll, c_void_p, c_char_p, c_size_t, wintypes, HRESULT, \
    create_string_buffer
from ctypes.wintypes import *

PVOID = LPVOID
PULONG = c_void_p
LPTSTR = c_void_p
LPBYTE = c_char_p
SIZE_T = c_size_t
HPCON = HANDLE

def _errcheck_bool(value, func, args):
    if not value:
        raise ctypes.WinError()
    return args


class STARTUPINFO(Structure):
    """ STARTUPINFO structure """
    _fields_ = [("cb", DWORD),
                ("lpReserved", LPTSTR),
                ("lpDesktop", LPTSTR),
                ("lpTitle", LPTSTR),
                ("dwX", DWORD),
                ("dwY", DWORD),
                ("dwXSize", DWORD),
                ("dwYSize", DWORD),
                ("dwXCountChars", DWORD),
                ("dwYCountChars", DWORD),
                ("dwFillAttribute", DWORD),
                ("dwFlags", DWORD),
                ("wShowWindow", WORD),
                ("cbReserved2", WORD),
                ("lpReserved2", LPBYTE),
                ("hStdInput", HANDLE),
                ("hStdOutput", HANDLE),
                ("hStdError", HANDLE)]


class STARTUPINFOEX(Structure):
    """ STARTUPINFOEX structure """
    _fields_ = [("StartupInfo", STARTUPINFO),
                ("lPAttributeList", POINTER(PVOID))]


class PROCESS_INFORMATION(Structure):
    """ PROCESS_INFORMATION structure """
    _fields_ = [("hProcess", HANDLE),
                ("hThread", HANDLE),
                ("dwProcessId", DWORD),
                ("dwThreadId", DWORD)]


class SECURITY_ATTRIBUTES(Structure):
    """ SECURITY_ATTRIBUTES structure """
    _fields_ = [("nLength", DWORD),
                ("lpSecurityDescriptor", HANDLE),
                ("bInheritHandle", DWORD)]


class COORD(Structure):
    """ COORD structure """
    _fields_ = [("X", SHORT),
                ("Y", SHORT)]


ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
DISABLE_NEWLINE_AUTO_RETURN = 0x0008
PROC_THREAD_ATTRIBUTE_PSEUDOCONSOLE = 0x00020016
EXTENDED_STARTUPINFO_PRESENT = 0x00080000
CREATE_NO_WINDOW = 0x08000000
STARTF_USESTDHANDLES = 0x00000100
BUFFER_SIZE_PIPE = 1048576

INFINITE = 0xFFFFFFFF
SW_HIDE = 0
GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002
FILE_ATTRIBUTE_NORMAL = 0x80
OPEN_EXISTING = 3
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12
INVALID_HANDLE_VALUE = -1

# BOOL InitializeProcThreadAttributeList(
#   LPPROC_THREAD_ATTRIBUTE_LIST lpAttributeList,
#   DWORD                        dwAttributeCount,
#   DWORD                        dwFlags,
#   PSIZE_T                      lpSize
# );
InitializeProcThreadAttributeList = windll.kernel32.InitializeProcThreadAttributeList
InitializeProcThreadAttributeList.argtype = [POINTER(HANDLE), POINTER(HANDLE), PVOID, DWORD]
InitializeProcThreadAttributeList.restype = BOOL
InitializeProcThreadAttributeList.errcheck = _errcheck_bool

# BOOL UpdateProcThreadAttribute(
#   LPPROC_THREAD_ATTRIBUTE_LIST lpAttributeList,
#   DWORD                        dwFlags,
#   DWORD_PTR                    Attribute,
#   PVOID                        lpValue,
#   SIZE_T                       cbSize,
#   PVOID                        lpPreviousValue,
#   PSIZE_T                      lpReturnSize
# );
UpdateProcThreadAttribute = windll.kernel32.UpdateProcThreadAttribute
UpdateProcThreadAttribute.argtype = [
    POINTER(PVOID),
    DWORD,
    POINTER(DWORD),
    PVOID,
    SIZE_T,
    PVOID,
    POINTER(SIZE_T)
]
UpdateProcThreadAttribute.restype = BOOL
UpdateProcThreadAttribute.errcheck = _errcheck_bool

# BOOL CreateProcessA(
#   LPCTSTR                 lpApplicationName,
#   LPTSTR                  lpCommandLine,
#   LPSECURITY_ATTRIBUTES   lpProcessAttributes,
#   LPSECURITY_ATTRIBUTES   lpThreadAttributes,
#   BOOL                    bInheritHandles,
#   DWORD                   dwCreationFlags,
#   LPVOID                  lpEnvironment,
#   LPCTSTR                 lpCurrentDirectory,
#   LPSTARTUPINFO           lpStartupInfo,
#   LPPROCESS_INFORMATION   lpProcessInformation,
#   );
CreateProcess = windll.kernel32.CreateProcessA
CreateProcess.restype = BOOL
CreateProcess.errcheck = _errcheck_bool

# BOOL CreateProcessW(
#   LPCWSTR               lpApplicationName,
#   LPWSTR                lpCommandLine,
#   LPSECURITY_ATTRIBUTES lpProcessAttributes,
#   LPSECURITY_ATTRIBUTES lpThreadAttributes,
#   BOOL                  bInheritHandles,
#   DWORD                 dwCreationFlags,
#   LPVOID                lpEnvironment,
#   LPCWSTR               lpCurrentDirectory,
#   LPSTARTUPINFOW        lpStartupInfo,
#   LPPROCESS_INFORMATION lpProcessInformation
# );
CreateProcessW = windll.kernel32.CreateProcessW  # <-- Unicode version!
CreateProcessW.restype = BOOL
CreateProcessW.errcheck = _errcheck_bool

# BOOL TerminateProcess(
#   INTPTR  hProcess,
#   UINT    uExitCode,
# );
TerminateProcess = windll.kernel32.TerminateProcess
TerminateProcess.restype = BOOL
TerminateProcess.errcheck = _errcheck_bool

# DWORD WaitForSingleObject(
#   HANDLE hHandle,
#   DWORD  dwMilliseconds
# );
WaitForSingleObject = ctypes.windll.kernel32.WaitForSingleObject
WaitForSingleObject.restype = ctypes.wintypes.DWORD
WaitForSingleObject.argtypes = (
    ctypes.wintypes.HANDLE,
    DWORD
)

# BOOL SetStdHandle(
#   DWORD nStdHandle
#   HANDLE hHandle,
# );
GetStdHandle = windll.kernel32.GetStdHandle
GetStdHandle.argtype = [
    DWORD,
    ctypes.wintypes.HANDLE,
]
GetStdHandle.restype = BOOL

# HANDLE GetStdHandle(
#   _In_ DWORD nStdHandle
# );
GetStdHandle = windll.kernel32.GetStdHandle
GetStdHandle.argtype = [DWORD]
GetStdHandle.restype = HANDLE

# BOOL CloseHandle(
#   HANDLE hObject
# );
CloseHandle = ctypes.windll.kernel32.CloseHandle
CloseHandle.argtypes = (
    HANDLE,  # hObject
)
CloseHandle.restype = ctypes.wintypes.BOOL
CloseHandle.errcheck = _errcheck_bool

# BOOL WINAPI CreatePipe(
#   _Out_    PHANDLE               hReadPipe,
#   _Out_    PHANDLE               hWritePipe,
#   _In_opt_ LPSECURITY_ATTRIBUTES lpPipeAttributes,
#   _In_     DWORD                 nSize
# );
CreatePipe = windll.kernel32.CreatePipe
CreatePipe.argtype = [POINTER(HANDLE), POINTER(HANDLE), PVOID, DWORD]
CreatePipe.restype = BOOL
CreatePipe.errcheck = _errcheck_bool

# HANDLE CreateFileW(
#   LPCWSTR               lpFileName,
#   DWORD                 dwDesiredAccess,
#   DWORD                 dwShareMode,
#   LPSECURITY_ATTRIBUTES lpSecurityAttributes,
#   DWORD                 dwCreationDisposition,
#   DWORD                 dwFlagsAndAttributes,
#   HANDLE                hTemplateFile
# );
CreateFileW = windll.kernel32.CreateFileW  # <-- Unicode version!
CreateFileW.restype = HANDLE
CreateFileW.argtype = [
    LPCWSTR,
    DWORD,
    DWORD,
    POINTER(c_void_p),
    DWORD,
    DWORD,
    HANDLE
]

# BOOL ReadFile(
#   HANDLE       hFile,
#   LPVOID       lpBuffer,
#   DWORD        nNumberOfBytesToRead,
#   LPDWORD      lpNumberOfBytesRead,
#   LPOVERLAPPED lpOverlapped
# );

ReadFile = ctypes.windll.kernel32.ReadFile
ReadFile.restype = ctypes.wintypes.BOOL
ReadFile.errcheck = _errcheck_bool
ReadFile.argtypes = (
    HANDLE,  # hObject
    LPVOID,
    DWORD,
    LPDWORD,
    POINTER(c_void_p)
)

# BOOL WriteFile(
#   HANDLE       hFile,
#   LPCVOID      lpBuffer,
#   DWORD        nNumberOfBytesToWrite,
#   LPDWORD      lpNumberOfBytesWritten,
#   LPOVERLAPPED lpOverlapped
# );
WriteFile = ctypes.windll.kernel32.WriteFile
WriteFile.restype = ctypes.wintypes.BOOL
WriteFile.errcheck = _errcheck_bool
WriteFile.argtypes = (
    HANDLE,
    LPCVOID,
    DWORD,
    LPDWORD,
    POINTER(c_void_p)
)

# HRESULT WINAPI CreatePseudoConsole(
#     _In_ COORD size,
#     _In_ HANDLE hInput,
#     _In_ HANDLE hOutput,
#     _In_ DWORD dwFlags,
#     _Out_ HPCON* phPC
# );
CreatePseudoConsole = windll.kernel32.CreatePseudoConsole
CreatePseudoConsole.argtype = [COORD, HANDLE, HANDLE, DWORD, POINTER(HPCON)]
CreatePseudoConsole.restype = HRESULT

# void WINAPI ClosePseudoConsole(
#     _In_ HPCON hPC
# );
ClosePseudoConsole = windll.kernel32.ClosePseudoConsole
ClosePseudoConsole.argtype = [HPCON]

# BOOL WINAPI SetConsoleMode(
#   _In_ HANDLE hConsoleHandle,
#   _In_ DWORD  dwMode
# );
SetConsoleMode = windll.kernel32.SetConsoleMode
SetConsoleMode.argtype = [HANDLE, DWORD]
SetConsoleMode.restype = BOOL
SetConsoleMode.errcheck = _errcheck_bool

# BOOL WINAPI GetConsoleMode(
#   _In_  HANDLE  hConsoleHandle,
#   _Out_ LPDWORD lpMode
# );
GetConsoleMode = windll.kernel32.GetConsoleMode
GetConsoleMode.argtype = [HANDLE, LPDWORD]
GetConsoleMode.restype = BOOL
# GetConsoleMode.errcheck = _errcheck_bool

# DECLSPEC_ALLOCATOR LPVOID HeapAlloc(
#   HANDLE hHeap,
#   DWORD  dwFlags,
#   SIZE_T dwBytes
# );
HeapAlloc = windll.kernel32.HeapAlloc
HeapAlloc.restype = LPVOID
HeapAlloc.argtypes = [HANDLE, DWORD, SIZE_T]

# BOOL HeapFree(
#   HANDLE                 hHeap,
#   DWORD                  dwFlags,
#   _Frees_ptr_opt_ LPVOID lpMem
# );
HeapFree = windll.kernel32.HeapFree
HeapFree.restype = BOOL
HeapFree.argtypes = [HANDLE, DWORD, LPVOID]
HeapFree.errcheck = _errcheck_bool

# HANDLE GetProcessHeap(
#
# );
GetProcessHeap = windll.kernel32.GetProcessHeap
GetProcessHeap.restype = HANDLE
GetProcessHeap.argtypes = []

# void WINAPI SetLastError(
#   _In_ DWORD dwErrCode
# );
SetLastError = windll.kernel32.SetLastError
SetLastError.argtype = [DWORD]

# void DeleteProcThreadAttributeList(
#   LPPROC_THREAD_ATTRIBUTE_LIST lpAttributeList
# );
DeleteProcThreadAttributeList = windll.kernel32.DeleteProcThreadAttributeList
DeleteProcThreadAttributeList.argtype = [
    POINTER(PVOID),
]

AllocConsole = windll.kernel32.AllocConsole
AllocConsole.restype = BOOL

FreeConsole = windll.kernel32.FreeConsole
FreeConsole.restype = BOOL

ShowWindow = windll.user32.ShowWindow
ShowWindow.argtype = [HANDLE, DWORD]
ShowWindow.restype = BOOL

GetConsoleWindow = windll.kernel32.GetConsoleWindow
GetConsoleWindow.restype = HANDLE

GetModuleHandle = windll.kernel32.GetModuleHandleA
GetModuleHandle.argtype = [LPCWSTR]
GetModuleHandle.restype = HANDLE

GetProcAddress = windll.kernel32.GetProcAddress
GetProcAddress.argtype = [HANDLE, LPCWSTR]
GetProcAddress.restype = HANDLE

null_ptr = POINTER(c_void_p)()

class ConPtyShell:

    def __init__(self, cols, rows):
        self._hpc = HPCON()
        self._pi = None
        self._ptyIn = wintypes.HANDLE(INVALID_HANDLE_VALUE)
        self._ptyOut = wintypes.HANDLE(INVALID_HANDLE_VALUE)
        self._cmdIn = wintypes.HANDLE(INVALID_HANDLE_VALUE)
        self._cmdOut = wintypes.HANDLE(INVALID_HANDLE_VALUE)

        # Create pipes
        CreatePipe(byref(self._ptyIn), byref(self._cmdIn), None, 0)
        CreatePipe(byref(self._cmdOut), byref(self._ptyOut), None, 0)

        # Create pseudo console
        self._consoleSize = COORD()
        self._consoleSize.X = cols
        self._consoleSize.Y = rows
        CreatePseudoConsole(self._consoleSize,  # ConPty Dimensions
                            self._ptyIn,        # ConPty Input
                            self._ptyOut,       # ConPty Output
                            DWORD(0),           # Flags
                            byref(self._hpc)    # ConPty Reference
                            )

        # Close the handles
        #CloseHandle(self._ptyIn)
        #CloseHandle(self._ptyOut)

    def _initAttachedToPseudoConsole(self, startupInfoEx):
        dwAttributeCount = 1
        dwFlags = 0
        lpSize = PVOID()

        # call with null lpAttributeList to get lpSize
        try:
            InitializeProcThreadAttributeList(None, dwAttributeCount, dwFlags, byref(lpSize))
        except WindowsError as err:
            if err.winerror == 122:
                # the data area passed to the system call is too small.
                SetLastError(0)
            else:
                raise

        mem = HeapAlloc(GetProcessHeap(), 0, lpSize.value)
        startupInfoEx.lpAttributeList = ctypes.cast(mem, ctypes.POINTER(c_void_p))

        InitializeProcThreadAttributeList(startupInfoEx.lpAttributeList, dwAttributeCount, dwFlags, byref(lpSize))
        UpdateProcThreadAttribute(startupInfoEx.lpAttributeList, DWORD(0), DWORD(PROC_THREAD_ATTRIBUTE_PSEUDOCONSOLE),
                                  self._hpc, sizeof(self._hpc), None, None)

        return mem

    def _pipe_handler(self):
        hConsole = GetStdHandle(STD_OUTPUT_HANDLE)

        BUF_SIZE = 512
        lpBuffer = create_string_buffer(BUF_SIZE)

        lpNumberOfBytesRead = DWORD()
        lpBytesWritten = DWORD()

        while True:
            lpNumberOfBytesRead.value = 0
            lpBytesWritten.value = 0

            try:
                ReadFile(self._ptyIn,                   # Handle to the file or i/o device
                         lpBuffer,                      # Pointer to the buffer that receive the data from the device
                         BUF_SIZE,                      # Maximum number of bytes to read
                         byref(lpNumberOfBytesRead),    # Number of bytes read from the device
                         null_ptr                       # Not used
                         )
                WriteFile(hConsole,                     # Handle to the file or i/o device
                          lpBuffer,                     # Pointer to the buffer that contains the data to be written
                          lpNumberOfBytesRead,          # Number of bytes to write
                          lpBytesWritten,               # Number of bytes written
                          null_ptr)                     # Not used
            except WindowsError as err:
                if err.winerror == 995:
                    return
                else:
                    raise

    def Read(self):
        MAX_READ = 1024*8
        lpBuffer = create_string_buffer(MAX_READ)
        lpNumberOfBytesRead = DWORD()
        ReadFile(self._ptyIn,
                 lpBuffer,
                 MAX_READ,
                 byref(lpNumberOfBytesRead),
                 null_ptr)
        print(f'read_size: {sizeof(lpBuffer)}')
        print(f'read_data: {lpBuffer.raw}')
        return lpBuffer.raw

    def Write(self, data):
        lpBuffer = create_string_buffer(data)
        lpNumberOfBytesWritten = DWORD()
        WriteFile(self._ptyOut,
                  lpBuffer,
                  sizeof(lpBuffer),
                  lpNumberOfBytesWritten,
                  null_ptr)

    def Close(self):
        CloseHandle(self._lpProcessInformation.hThread)
        CloseHandle(self._lpProcessInformation.hProcess)
        DeleteProcThreadAttributeList(self._startupInfoEx.lpAttributeList)
        HeapFree(GetProcessHeap(), 0, self._mem)
        ClosePseudoConsole(self._hpc)
        CloseHandle(self._ptyOut)
        CloseHandle(self._ptyIn)
        CloseHandle(self._cmdOut)
        CloseHandle(self._cmdIn)

    def Start(self):

        # todo: check to make sure that this version of windows supports ConPty
        #t = threading.Thread(target=lambda: self._pipe_handler())
        #t.start()


        # todo: create console and attach to pty
        self._startupInfoEx = STARTUPINFOEX()
        self._startupInfoEx.StartupInfo.cb = sizeof(STARTUPINFOEX)

        self._mem = self._initAttachedToPseudoConsole(self._startupInfoEx)

        self._lpProcessInformation = PROCESS_INFORMATION()

        CreateProcessW(None,                                        # _In_opt_      LPCTSTR
                       "powershell.exe",                            # _Inout_opt_   LPTSTR
                       None,                                        # _In_opt_      LPSECURITY_ATTRIBUTES
                       None,                                        # _In_opt_      LPSECURITY_ATTRIBUTES
                       False,                                       # _In_          BOOL
                       EXTENDED_STARTUPINFO_PRESENT,                # _In_          DWORD
                       None,                                        # _In_opt_      LPVOID
                       None,                                        # _In_opt_      LPCTSTR
                       byref(self._startupInfoEx.StartupInfo),      # _In_          LPSTARTUPINFO
                       byref(self._lpProcessInformation))           # _Out_         LPPROCESS_INFORMATION

        WaitForSingleObject(self._lpProcessInformation.hThread, 100 * 1000)



        time.sleep(100)
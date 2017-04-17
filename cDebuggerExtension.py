import os, re;

gsThisFilePath = os.path.dirname(__file__);
gdsDebuggerExtensionDLLPath_by_sCdbISA = {
  "x86": os.path.join(gsThisFilePath, "DebuggerExtension", "bin", "i386", "debugext.dll"),
  "x64": os.path.join(gsThisFilePath, "DebuggerExtension", "bin", "amd64", "debugext.dll"),
};

class cDebuggerExtension(object):
  @staticmethod
  def foLoad(oCdbWrapper):
    sDebuggerExtensionDLLPath = gdsDebuggerExtensionDLLPath_by_sCdbISA[oCdbWrapper.sCdbISA];
    asLoadOutput = oCdbWrapper.fasSendCommandAndReadOutput(
      '.load "%s"' % sDebuggerExtensionDLLPath.replace("\\", "\\\\").replace('"', '\\"')
    );
    if not oCdbWrapper.bCdbRunning: return;
    assert not asLoadOutput, \
        "Failed to load debugger extension %s:\r\n%s" % (sDebuggerExtensionDLLPath, "\r\n".join(asLoadOutput));
    return cDebuggerExtension(oCdbWrapper);
  
  def __init__(oDebuggerExtension, oCdbWrapper):
    oDebuggerExtension.oCdbWrapper = oCdbWrapper;
  
  def fuSetVirtualAllocationProtection(oDebuggerExtension, uAddress, uSize, uProtection, sComment):
    oCdbWrapper = oDebuggerExtension.oCdbWrapper;
    asProtectResult = oCdbWrapper.fasSendCommandAndReadOutput(
      "!Protect 0x%X 0x%X 0x%X; $ %s" % (uAddress, uSize, uProtection, sComment)
    );
    if not oCdbWrapper.bCdbRunning: return;
    assert len(asProtectResult) > 0, \
        "!Protect did not return any results.";
    if len(asProtectResult) == 1 and re.match(r"^Protect: (OpenProcess|VirtualProtectEx) failed with error code \d+$", asProtectResult[0]):
      return None;
    uOldProtection = None;
    uNewProtection = None;
    assert len(asProtectResult) == 2, \
        "Expected !Protect output to be 2 lines, not %d:\r\n%s" % (len(asProtectResult), "\r\n".join(asProtectResult));
    oNewProtectionMatch = re.match(r"^New protection \((\d+)\)$", asProtectResult[0]); # first line has new protection flag
    assert oNewProtectionMatch and long(oNewProtectionMatch.group(1)) == uProtection, \
        'Expected !Protect output to start with "New protection (number):\r\n%s' % "\r\n".join(asProtectResult);
    oOldProtectionMatch = re.match(r"^Old protection \((\d+)\)$", asProtectResult[1]); # second line has old protection flag
    assert oOldProtectionMatch, \
        'Expected !Protect output to end with "Old protection (number):\r\n%s' % "\r\n".join(asProtectResult);
    return long(oOldProtectionMatch.group(1));
  

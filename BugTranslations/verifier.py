import re;
from cBugTranslation import cBugTranslation;

aoBugTranslations = [
  # All these are never relevant to the bug
  cBugTranslation(
    aasAdditionalIrrelevantStackFrameSymbols = [
      [
        "verifier.dll!AVrfDebugPageHeapAllocate",
      ], [
        "verifier.dll!AVrfDebugPageHeapFree",
      ], [
        "verifier.dll!AVrfpDphCheckNormalHeapBlock",
      ], [
        "verifier.dll!AVrfpDphFindBusyMemory",
      ], [
        "verifier.dll!AVrfpDphFindBusyMemoryAndRemoveFromBusyList",
      ], [
        "verifier.dll!AVrfpDphFindBusyMemoryNoCheck",
      ], [
        "verifier.dll!AVrfpDphNormalHeapFree",
      ], [
        "verifier.dll!AVrfpDphRaiseException",
      ], [
        "verifier.dll!AVrfpDphReportCorruptedBlock",
      ], [
        "verifier.dll!VerifierStopMessage",
      ],
    ],
  ),
];

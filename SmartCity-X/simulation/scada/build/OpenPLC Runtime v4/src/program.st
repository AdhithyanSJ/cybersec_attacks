PROGRAM main
  VAR
    Breaker_Status : BOOL;
    Grid_Online : BOOL;
    Emergency : BOOL;
    Load_Percent : INT;
    Voltage_kV : REAL;
    Frequency_Hz : REAL;
  END_VAR
  VAR
    Breaker_Command AT %MW0 : INT;
  END_VAR

  (* ========================================= *)
  (* SMARTCITY-X SUBSTATION CONTROL LOGIC     *)
  (* ========================================= *)

  (* Breaker follows the SCADA command *)

  IF Breaker_Command = 1 THEN

      Breaker_Status := TRUE;
      Grid_Online := TRUE;
      Emergency := FALSE;

      Load_Percent := 72;
      Voltage_kV := 230.0;
      Frequency_Hz := 50.0;

  ELSIF Breaker_Command = 0 THEN

      Breaker_Status := FALSE;
      Grid_Online := FALSE;
      Emergency := TRUE;

      Load_Percent := 0;
      Voltage_kV := 0.0;
      Frequency_Hz := 0.0;

  END_IF;
END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#20ms,PRIORITY := 1);
    PROGRAM instance0 WITH task0 : main;
  END_RESOURCE
END_CONFIGURATION

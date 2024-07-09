import unittest 
import os.path
from tag_generator.base.file_functions import *
from deepdiff import DeepDiff
from unittest.mock import MagicMock

class Test_File_Functions(unittest.TestCase):
    def test_get_basename_without_extension(self):
        file_path = 'test_file.txt'
        self.assertEqual(get_basename_without_extension(file_path), 'test_file')

    def test_get_all_files(self):
        dir = os.path.join('src','tests','files','input', 'mitsubishi')
        extension = '.json'
        expected_output = [
            os.path.join('src', 'tests', 'files', 'input', 'mitsubishi', 'json', 'FITBasePanConveyor.json'),
            os.path.join('src', 'tests', 'files', 'input', 'mitsubishi', 'json', 'Kaishi_Conv_tags.json'),
            os.path.join('src', 'tests', 'files', 'input', 'mitsubishi', 'json', 'Kansei_Conv_tags.json'),
            os.path.join('src', 'tests', 'files', 'input', 'mitsubishi', 'json', 'RFID_HIPOT_tags.json'),
            os.path.join('src', 'tests', 'files', 'input', 'mitsubishi', 'json', 'RFID_LT1_tags.json'),
            os.path.join('src', 'tests', 'files', 'input', 'mitsubishi', 'json', 'RFID_PD1_tags.json'),
            os.path.join('src', 'tests', 'files', 'input', 'mitsubishi', 'json', 'RFID_RC1_tags.json')
        ]
        
        output = get_all_files(dir, extension)

        diff = DeepDiff(expected_output, output, ignore_order=True, verbose_level=2)
        if diff:
            self.fail(f"Output does not match expected output: {diff}")

    def test_get_dict_from_json_files(self):
        # Mock the logger object
        logger_mock = MagicMock()

        # Define the input JSON files
        json_files = [
            os.path.join('src', 'tests', 'files', 'input', 'mitsubishi', 'json', 'FITBasePanConveyor.json')
        ]

        # Define the expected output dictionary
        expected_output = {
            'FITBasePanConveyor': {
            "name": "FITBasePanConveyor",
            "tagType": "Folder",
            "tags": [
                {
                "valueSource": "memory",
                "name": "REQUEST_PARTS_MATCH_NEW",
                "value": 0,
                "tagType": "AtomicTag"
                },
                {
                "valueSource": "opc",
                "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_UnitInfo_Revision",
                "dataType": "String",
                "name": "REVISION",
                "tagGroup": "AFP01_Normal",
                "tagType": "AtomicTag",
                "opcServer": "FIT_Kepware"
                },
                {
                "valueSource": "opc",
                "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_UnitInfo_SerialNo",
                "dataType": "String",
                "historyProvider": "IGN_DB_FIT",
                "historicalDeadband": 0.5,
                "historicalDeadbandStyle": "Discrete",
                "name": "SERIALNO",
                "historyEnabled": True,
                "tagGroup": "AFP01_Normal",
                "tagType": "AtomicTag",
                "opcServer": "FIT_Kepware"
                },
                {
                "valueSource": "memory",
                "readOnly": True,
                "dataType": "String",
                "name": "AMSEndpoint",
                "readPermissions": {
                    "type": "AllOf",
                    "securityLevels": [
                    {
                        "name": "Authenticated",
                        "children": []
                    }
                    ]
                },
                "value": "http://10.172.86.148/afp01",
                "tagGroup": "AFP01_Normal",
                "tagType": "AtomicTag"
                },
                {
                "valueSource": "opc",
                "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.PHS_PLC_Heartbeat",
                "dataType": "Int2",
                "name": "PHS_PLC_Heartbeat",
                "tagGroup": "AFP01_Normal",
                "tagType": "AtomicTag",
                "opcServer": "FIT_Kepware"
                },
                {
                "valueSource": "memory",
                "readOnly": True,
                "dataType": "String",
                "name": "TESTID",
                "value": "SA_BASEPAN_CMP_PM",
                "tagGroup": "AFP01_Normal",
                "tagType": "AtomicTag"
                },
                {
                "valueSource": "opc",
                "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_UnitInfo_ModelName",
                "dataType": "String",
                "historyProvider": "IGN_DB_FIT",
                "historicalDeadband": 0.5,
                "historicalDeadbandStyle": "Discrete",
                "name": "MODELNO",
                "historyEnabled": True,
                "tagGroup": "AFP01_Normal",
                "tagType": "AtomicTag",
                "opcServer": "FIT_Kepware"
                },
                {
                "name": "RECIPE_RESPONSE",
                "tagType": "Folder",
                "tags": [
                    {
                    "valueSource": "opc",
                    "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_Recipe_LocatorYPosition",
                    "dataType": "Int4",
                    "name": "LOCATOR_Y_POSITION",
                    "tagGroup": "AFP01_Normal",
                    "tagType": "AtomicTag",
                    "opcServer": "FIT_Kepware"
                    },
                    {
                    "valueSource": "opc",
                    "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_Recipe_Diameter",
                    "dataType": "Int4",
                    "name": "COMPRESSOR_DIAMETER",
                    "tagGroup": "AFP01_Normal",
                    "tagType": "AtomicTag",
                    "opcServer": "FIT_Kepware"
                    },
                    {
                    "valueSource": "opc",
                    "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_Recipe_Weight",
                    "dataType": "Int4",
                    "name": "COMPRESSOR_WEIGHT",
                    "tagGroup": "AFP01_Normal",
                    "tagType": "AtomicTag",
                    "opcServer": "FIT_Kepware"
                    },
                    {
                    "valueSource": "opc",
                    "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_Recipe_RobotSetDownPR1",
                    "dataType": "Int4",
                    "name": "ROBOT_SET_DOWN_1_PR",
                    "tagGroup": "AFP01_Normal",
                    "tagType": "AtomicTag",
                    "opcServer": "FIT_Kepware"
                    },
                    {
                    "valueSource": "opc",
                    "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_Recipe_Height",
                    "dataType": "Int4",
                    "name": "COMPRESSOR_HEIGHT",
                    "tagGroup": "AFP01_Normal",
                    "tagType": "AtomicTag",
                    "opcServer": "FIT_Kepware"
                    },
                    {
                    "valueSource": "opc",
                    "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_GetRecipe_PHSOK",
                    "dataType": "Int2",
                    "historyProvider": "IGN_DB_FIT",
                    "historicalDeadband": 0.5,
                    "historicalDeadbandStyle": "Discrete",
                    "name": "PHS_OK",
                    "historyEnabled": True,
                    "tagGroup": "AFP01_Normal",
                    "tagType": "AtomicTag",
                    "opcServer": "FIT_Kepware"
                    },
                    {
                    "valueSource": "opc",
                    "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_Recipe_ReceipeNumber",
                    "dataType": "Int4",
                    "name": "RECIPE_NUMBER",
                    "tagGroup": "AFP01_Normal",
                    "tagType": "AtomicTag",
                    "opcServer": "FIT_Kepware"
                    },
                    {
                    "valueSource": "opc",
                    "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_Recipe_PayloadNumber",
                    "dataType": "Int4",
                    "name": "PAYLOAD_NUMBER",
                    "tagGroup": "AFP01_Normal",
                    "tagType": "AtomicTag",
                    "opcServer": "FIT_Kepware"
                    },
                    {
                    "valueSource": "opc",
                    "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_GetRecipe_Message",
                    "dataType": "String",
                    "historyProvider": "IGN_DB_FIT",
                    "historicalDeadband": 0.5,
                    "historicalDeadbandStyle": "Discrete",
                    "name": "message",
                    "historyEnabled": True,
                    "tagGroup": "AFP01_Normal",
                    "tagType": "AtomicTag",
                    "opcServer": "FIT_Kepware"
                    },
                    {
                    "valueSource": "opc",
                    "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_Recipe_UnitType",
                    "dataType": "String",
                    "name": "UNIT_TYPE",
                    "tagGroup": "AFP01_Normal",
                    "tagType": "AtomicTag",
                    "opcServer": "FIT_Kepware"
                    },
                    {
                    "valueSource": "opc",
                    "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_Recipe_RobotPickupPR0",
                    "dataType": "Int4",
                    "name": "ROBOT_PICKUP_1_PR",
                    "tagGroup": "AFP01_Normal",
                    "tagType": "AtomicTag",
                    "opcServer": "FIT_Kepware"
                    },
                    {
                    "valueSource": "opc",
                    "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_GetRecipe_ReturnCode",
                    "dataType": "Int2",
                    "historyProvider": "IGN_DB_FIT",
                    "historicalDeadband": 0.5,
                    "historicalDeadbandStyle": "Discrete",
                    "name": "returnCode",
                    "historyEnabled": True,
                    "tagGroup": "AFP01_Normal",
                    "tagType": "AtomicTag",
                    "opcServer": "FIT_Kepware"
                    },
                    {
                    "valueSource": "opc",
                    "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_Recipe_LocatorXPosition",
                    "dataType": "Int4",
                    "name": "LOCATOR_X_POSITION",
                    "tagGroup": "AFP01_Normal",
                    "tagType": "AtomicTag",
                    "opcServer": "FIT_Kepware"
                    },
                    {
                    "valueSource": "opc",
                    "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_Recipe_BasePanModelNumber",
                    "dataType": "String",
                    "historyProvider": "IGN_DB_FIT",
                    "historicalDeadband": 0.5,
                    "historicalDeadbandStyle": "Discrete",
                    "name": "BASEPAN_NUMBER",
                    "historyEnabled": True,
                    "tagGroup": "AFP01_Normal",
                    "tagType": "AtomicTag",
                    "opcServer": "FIT_Kepware"
                    }
                ]
                },
                {
                "valueSource": "memory",
                "readOnly": True,
                "dataType": "String",
                "name": "PartsMatchEndpoint",
                "readPermissions": {
                    "type": "AllOf",
                    "securityLevels": [
                    {
                        "name": "Authenticated",
                        "children": []
                    }
                    ]
                },
                "value": "http://10.172.86.148/afp01/WebApi/request-parts-match",
                "tagGroup": "AFP01_Normal",
                "tagType": "AtomicTag"
                },
                {
                "valueSource": "opc",
                "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor._System._NoError",
                "alarms": [
                    {
                    "activePipeline": "FIT_Main/NoCommNotifications",
                    "CustomEmailMessage": "FIT BasePan Conveyor PLC Disconnected",
                    "name": "FITBasePanConvDisconnected",
                    "clearPipeline": "FIT_Main/NoCommNotifications",
                    "CustomEmailSubject": "FIT PLC Disconnected Alarm"
                    }
                ],
                "name": "IsConnected",
                "tagGroup": "AFP01_Normal",
                "tagType": "AtomicTag",
                "opcServer": "FIT_Kepware"
                },
                {
                "valueSource": "opc",
                "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_RequestGetRecipe",
                "historicalDeadband": 0.5,
                "historicalDeadbandStyle": "Discrete",
                "tagGroup": "AFP01_Normal",
                "tagType": "AtomicTag",
                "enabled": True,
                "dataType": "Int2",
                "historyProvider": "IGN_DB_FIT",
                "name": "REQUEST_GET_RECIPE",
                "historyEnabled": True,
                "opcServer": "FIT_Kepware"
                },
                {
                "valueSource": "opc",
                "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_RequestOKToTest",
                "dataType": "Int2",
                "historyProvider": "IGN_DB_FIT",
                "historicalDeadband": 0.5,
                "historicalDeadbandStyle": "Discrete",
                "name": "REQUEST_PARTS_MATCH",
                "historyEnabled": True,
                "tagGroup": "AFP01_Normal",
                "tagType": "AtomicTag",
                "opcServer": "FIT_Kepware"
                },
                {
                "name": "PARTS_MATCH_RESPONSE",
                "tagType": "Folder",
                "tags": [
                    {
                    "valueSource": "opc",
                    "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_IsOKToTest_Message",
                    "historicalDeadband": 0.5,
                    "historicalDeadbandStyle": "Discrete",
                    "tagGroup": "AFP01_Normal",
                    "tagType": "AtomicTag",
                    "readOnly": True,
                    "dataType": "String",
                    "historyProvider": "IGN_DB_FIT",
                    "name": "message",
                    "historyEnabled": True,
                    "opcServer": "FIT_Kepware"
                    },
                    {
                    "valueSource": "opc",
                    "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_IsOKToTest_PHSOK",
                    "dataType": "Int2",
                    "historyProvider": "IGN_DB_FIT",
                    "historicalDeadband": 0.5,
                    "historicalDeadbandStyle": "Discrete",
                    "name": "PHS_OK",
                    "historyEnabled": True,
                    "tagGroup": "AFP01_Normal",
                    "tagType": "AtomicTag",
                    "opcServer": "FIT_Kepware"
                    },
                    {
                    "valueSource": "opc",
                    "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_IsOKToTest_ReturnCode",
                    "dataType": "Int2",
                    "historyProvider": "IGN_DB_FIT",
                    "historicalDeadband": 0.5,
                    "historicalDeadbandStyle": "Discrete",
                    "name": "returnCode",
                    "historyEnabled": True,
                    "tagGroup": "AFP01_Normal",
                    "tagType": "AtomicTag",
                    "opcServer": "FIT_Kepware"
                    }
                ]
                },
                {
                "valueSource": "memory",
                "name": "REQUEST_GET_RECIPE_NEW",
                "value": 0,
                "tagType": "AtomicTag"
                },
                {
                "valueSource": "opc",
                "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_ConfirmData",
                "dataType": "Int2",
                "name": "CONFIRM",
                "tagGroup": "AFP01_Normal",
                "tagType": "AtomicTag",
                "opcServer": "FIT_Kepware"
                },
                {
                "name": "RESULTS",
                "tagType": "Folder",
                "tags": [
                    {
                    "valueSource": "opc",
                    "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_IsOKToTest_ReturnCode",
                    "dataType": "Int2",
                    "name": "returnCode",
                    "tagGroup": "AFP01_Normal",
                    "tagType": "AtomicTag",
                    "opcServer": "FIT_Kepware"
                    },
                    {
                    "valueSource": "opc",
                    "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_IsOKToTest_Message",
                    "dataType": "String",
                    "name": "message",
                    "tagGroup": "AFP01_Normal",
                    "tagType": "AtomicTag",
                    "opcServer": "FIT_Kepware"
                    },
                    {
                    "valueSource": "opc",
                    "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_IsOKToTest_PHSOK",
                    "dataType": "Int2",
                    "name": "PHS_OK",
                    "tagGroup": "AFP01_Normal",
                    "tagType": "AtomicTag",
                    "opcServer": "FIT_Kepware"
                    },
                    {
                    "valueSource": "opc",
                    "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Grommet_TestResult_CycleTime",
                    "dataType": "String",
                    "name": "CycleTime",
                    "tagGroup": "AFP01_Normal",
                    "tagType": "AtomicTag",
                    "opcServer": "FIT_Kepware"
                    },
                    {
                    "valueSource": "opc",
                    "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_TestResult_ProcessingResult",
                    "dataType": "String",
                    "name": "ProcessingResult",
                    "tagGroup": "AFP01_Normal",
                    "tagType": "AtomicTag",
                    "opcServer": "FIT_Kepware"
                    },
                    {
                    "valueSource": "opc",
                    "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.Compressor_TestResult_NGCode",
                    "dataType": "String",
                    "name": "NGCode",
                    "tagGroup": "AFP01_Normal",
                    "tagType": "AtomicTag",
                    "opcServer": "FIT_Kepware"
                    }
                ]
                },
                {
                "valueSource": "opc",
                "opcItemPath": "nsu\u003dThingWorx Kepware Server;s\u003dSA_BasePanConveyor.SA_BasePanConveyor.PARTBARCODE1",
                "dataType": "String",
                "historyProvider": "IGN_DB_FIT",
                "historicalDeadband": 0.01,
                "historicalDeadbandStyle": "Discrete",
                "name": "PARTBARCODE",
                "historyEnabled": True,
                "tagGroup": "AFP01_Normal",
                "tagType": "AtomicTag",
                "opcServer": "FIT_Kepware"
                },
                {
                "valueSource": "expr",
                "eventScripts": [
                    {
                    "eventid": "valueChanged",
                    "script": "\tif currentValue !\u003d previousValue:\n\t\tsystem.tag.writeBlocking([\"[~]PHS_PLC_Heartbeat\"], currentValue.value)"
                    }
                ],
                "expression": "if(getSecond(now(1000))%2 \u003d 0, 1,0)",
                "name": "Heartbeat",
                "tagGroup": "AFP01_Normal",
                "tagType": "AtomicTag"
                },
                {
                "valueSource": "reference",
                "sourceTagPath": "[~]AMSOperation/Andon/AFP01/BASEPAN_CONV/SA_BasepanCVPB_Running ",
                "name": "IsRunning",
                "historyEnabled": True,
                "tagGroup": "AFP01_Normal",
                "tagType": "AtomicTag"
                },
                {
                "valueSource": "memory",
                "dataType": "String",
                "name": "TESTTYPE",
                "value": "FIT_AFP01_COMPRESSOR_ROBOT",
                "tagGroup": "AFP01_Normal",
                "tagType": "AtomicTag"
                }
            ]
            }
        }

        actual_output = get_dict_from_json_files(json_files)

        # Compare the actual output with the expected output
        diff = DeepDiff(expected_output, actual_output, ignore_order=True, verbose_level=2)
        if diff:
            self.fail(f"Output does not match expected output: {diff}")
    





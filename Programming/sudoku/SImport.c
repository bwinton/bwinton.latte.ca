/* SImport.c */
#ifdef __GNUC__
#    include <PalmOS.h>    // for PRC Tool compatability
#endif

// PalmOS Functions.
void LstDrawList( ListType *pList )
	SYS_TRAP(sysTrapLstDrawList);
Int16 LstGetNumberOfItems( ListType *pList )
	SYS_TRAP(sysTrapLstGetNumberOfItems);
Boolean LstScrollList( ListType *pList, WinDirectionType d, Int16 count )
	SYS_TRAP(sysTrapLstScrollList);
UInt32 MemPtrSize( MemPtr p )
	SYS_TRAP(sysTrapMemPtrSize);
Err SysAppLaunch( UInt16 cardNo, LocalID dbID, UInt16 launchFlags,
	UInt16 cmd, MemPtr cmdPBP, UInt32 *resultP )
	SYS_TRAP(sysTrapSysAppLaunch);
Err DmRecordInfo( DmOpenRef db, UInt16 i, UInt16 *attr, UInt32 *uid, LocalID *chunk )
	SYS_TRAP(sysTrapDmRecordInfo);
void CategoryGetName( DmOpenRef db, UInt16 i, Char *name )
	SYS_TRAP(sysTrapCategoryGetName);
void CategorySetTriggerLabel( ControlType *ctl, Char *name )
	SYS_TRAP(sysTrapCategorySetTriggerLabel);
Boolean CategorySelect( DmOpenRef db, FormType *, UInt16 tid, UInt16 lid, Boolean title, UInt16 *index,
	Char *name, UInt8 unEdit, UInt32 strId )
	SYS_TRAP(sysTrapCategorySelect);
UInt16 DmNumRecordsInCategory( DmOpenRef db, UInt16 category )
	SYS_TRAP(sysTrapDmNumRecordsInCategory);
MemHandle DmQueryNextInCategory( DmOpenRef db, UInt16 *i, UInt16 category)
	SYS_TRAP(sysTrapDmQueryNextInCategory);

#define dmCategoryLength				16
#define dmAllCategories					0xff
#define dmRecAttrCategoryMask		0x0f
#define categoryDefaultEditCategoryString	10001
#define noListSelection					-1

// Add a record to an application's database.
#define sysAppLaunchCmdAddRecord	19

// Resource ids.
#define MainForm						1000
#define AboutAlert						1000
#define DebugAlert						1100
#define MemoList						1001
#define CategoryList					1010
#define CategoryTrigger				1011
#define MainFormImportButton	1100

// Actions.  (Menu & Button IDs)
#define DisplayAbout					1000
#define ImportFromMemo			1100

// Errors
#define ERR_NO_TITLE_LINE 101
#define ERR_TITLE_LINE_AT_END_OF_MEMO 102
#define ERR_NO_TITLE 103
#define ERR_MISSING_NEWLINE_ON_NON_LAST_LINE 104
#define ERR_UNKNOWN_CHAR_IN_PUZZLE 105
#define ERR_COULD_NOT_FIND_SUDOKU_APP 106
#define ERR_NO_MEMODB 107

#define creatorID	'SImp'
#define versionID	1

UInt32 textSize = 50;

// Prototypes
typedef struct GameRecord
{
    Char title[22];
    UInt16 cells[81];
    UInt32 time;
} GameRecord;

typedef struct SImportPrefs
{
    UInt16 CurrentCategory;
} SImportPrefs;

static Boolean appHandleEvent (EventPtr pEvent);
static void    mainFormInit (FormPtr pForm);
static Boolean mainFormEventHandler (EventPtr pEvent);
static Boolean doMainAction (FormPtr pForm, UInt16 command);
static Boolean doMainControl (FormPtr pForm, UInt16 ctl);
static Boolean doMainKey (FormPtr pForm, WChar chr);
static void updateList( FormPtr pForm  );
void * getObjectPtr (FormPtr pForm, Int16 resourceNo);
Err findNextRecord( Char** data );
Err readRecord( GameRecord *newRecord, Char** data );
Err addRecord( GameRecord* newRecord );
Char ** items;
UInt32 recordC;
Char categoryName [dmCategoryLength];
DmOpenRef memoDb;
SImportPrefs gPrefs;


// Code
static Err startApp()
{
    //PrefGetAppPreferences
    UInt16 nAppPrefsSize;
    if ( PrefGetAppPreferences(creatorID, 0, &gPrefs, &nAppPrefsSize, true) == noPreferenceFound )
    {
        MemSet(&gPrefs, sizeof(gPrefs), 0);
        gPrefs.CurrentCategory = dmAllCategories; 
    }
    memoDb = DmOpenDatabaseByTypeCreator(
        'DATA', 'PMem', dmModeReadOnly );
     if ( memoDb == 0 )
    {
         // We might be on an old device, so try the standard memo database.
        memoDb = DmOpenDatabaseByTypeCreator(
            'DATA', 'memo', dmModeReadOnly );
    }
    // If it's still 0, we can't find it.
    if ( memoDb == 0 )
    {
          return ERR_NO_MEMODB;
    }
    return errNone;
}

static void stopApp()
{
    PrefSetAppPreferences(creatorID, 0, versionID, &gPrefs, sizeof(gPrefs), true);
    Err err = DmCloseDatabase( memoDb );
     if ( err != errNone )
     {
         // StrPrintF( message, "Close Error" );
         break;
     }
     return;
}

/*
 * Entry point for the application.
 */
UInt32 PilotMain( UInt16  cmd, void *cmdPBP, UInt16 launchFlags )
{
    EventType    event;
    UInt16       error;
    if (cmd == sysAppLaunchCmdNormalLaunch)
    {
        items = NULL;
        Err err = startApp();
        if ( err != errNone )
        {
            return err;
        }
        FrmGotoForm(MainForm);
        do
        {
            // Wait for an event
            EvtGetEvent(&event, evtWaitForever);
            // ask event handlers, in turn, to deal with the event.
            if (!SysHandleEvent (&event))
            if (!MenuHandleEvent (0, &event, &error))
            if (!appHandleEvent (&event))
                FrmDispatchEvent (&event);
        } while (event.eType != appStopEvent);
        stopApp();
        FrmCloseAllForms();
	   if (items != NULL)
	    {  
	        for ( UInt8 i=0; i<recordC; i++ )
	        {
	            MemPtrFree( items[i] );
	        }
	        MemPtrFree( items );
	        items = NULL;
	    }
    }
    return 0;
}

/*
 * Top-level event handler for the application.
 */
static Boolean appHandleEvent (EventPtr pEvent)
{
    FormPtr pForm;
    Int16   formId;
    Boolean handled = false;
    if (pEvent->eType == frmLoadEvent)
    {
        // Load the resource for the form
        formId = pEvent->data.frmLoad.formID;
        pForm  = FrmInitForm(formId);
        FrmSetActiveForm(pForm);
        // install a form-specific event handler
        if (formId == MainForm)
        {
            FrmSetEventHandler( pForm, mainFormEventHandler );
        }
        // *** ADD NEW FORM HANDLING HERE *** //
        handled = true;
    }
    return handled;
}

/*
 * Add all the Sudokus from a memo to the Sudoku Database.
 */
Err processRecord( MemPtr recordP, int *puzzles )
{
    Err err = errNone;
    UInt32 dataSize = MemPtrSize( recordP );
    Char* data = (Char *)MemPtrNew( dataSize );
    GameRecord newRecord;
    if ( data == NULL )
    {
        err = 7;
        return err;
    }
    err = MemMove( data, recordP, dataSize );
    if ( err != errNone )
    {
        MemPtrFree( data );
        return 800+err;
    }
    Char* line = data;
    while ( (line != NULL) && (line <= data + dataSize) )
    {
        err = findNextRecord( &line );
        if ( err == ERR_NO_TITLE_LINE )
        {
            if ( (*puzzles) > 0 )
            {
                // We expect this error for the last record,
                // so convert it to ernNone.
                err = errNone;
            }
            break;
        }
        if ( err == errNone )
        {
            err = readRecord( &newRecord, &line );
        }
        if ( err == errNone )
        {
            err = addRecord( &newRecord );
            (*puzzles)++;
        }
    }
    MemPtrFree( data );
    return err;
}

/*
 * Find the next Sudoku in a memo, by searching for a
 * title line that starts with '% '.
 */
Err findNextRecord( Char** lineP )
{
    Err err = errNone;
    Char* line = *lineP;
    while ( *line != '%' || *(line+1) != ' ' )
    {
        line = StrChr( line, 10 );
        if ( line == NULL )
        {
            err = ERR_NO_TITLE_LINE;
            *lineP = NULL;
            return err;
        }
        line++;
    }
    line = line + 2;
    *lineP = line;
    return err;
}

/*
 * Add a cell to a Sudoku GameRecord.
 *
 * @param value - The character representation ofthe cell.
 * @param newRecord - The record to populate.
 * @param index - The index ofthe cell to populate.
 */
Err addCell( Char value, GameRecord *newRecord, int index )
{
    Err err = errNone;
    if ( value >='1' && value <= '9' )
    {
        newRecord->cells[index] = 0x0200;
        newRecord->cells[index] |= 1 << (value-'1');
    }
    else if ( value == '.'  || value == '0' )
    {
        newRecord->cells[index] = 0x00;
    }
    else
    {
        err = ERR_UNKNOWN_CHAR_IN_PUZZLE;
        Char msg[30];
        StrPrintF( msg, "Unknown Char %d at %d.", value, index );
        FrmCustomAlert( DebugAlert, msg, "","" );
    }
    return err;
}

/*
 * Populate a Sudoku GameRecord from a puzzle in the memo.
 *
 * @param newRecord - The record to populate.
 * @param lineP - A pointer to the pointer to the first character of the title.
 */
Err readRecord( GameRecord *newRecord, Char** lineP )
{
    Err err = errNone;
    Char* line = *lineP;
    Char* nextLine = StrChr( line, 10 );
    if ( nextLine == NULL )
    {
        err = ERR_TITLE_LINE_AT_END_OF_MEMO;
        *lineP = NULL;
        return err;
    }
    *nextLine = 0;
    if ( StrLen( line ) == 0 )
    {
        err = ERR_NO_TITLE;
        *lineP = nextLine+1;
        return err;
    }
    MemMove( newRecord->title, line, 21 );
    newRecord->title[21] = 0;
    newRecord->time = 0;

    line = nextLine+1;
    nextLine = StrChr( line, 10 );
    int length = 0;
    if ( nextLine == NULL )
    {
        length = StrLen( line );
    }
    else
    {
        length = nextLine - line;
    }

    if ( length == 81 )
    {
         for ( int j=0; j<81; j++ )
         {
             err = addCell( line[j], newRecord, j );
             if ( err != errNone )
             {
                 *lineP = line;
                 return err;
             }
         } // for ( int j=0; j<81; j++ )
         line = nextLine+1;
    }
    else if ( length == 9 )
    {
        for ( int i=0; i<9; i++ )
        {
            for ( int j=0; j<9; j++ )
            {
                err = addCell( line[j], newRecord, i*9+j );
                if ( err != errNone )
                {
                    *lineP = line;
                    return err;
                }
            } // for ( int j=0; i<9; j++ )
            line = nextLine+1;
            nextLine = StrChr( line, 10 );
        } // for ( int i=0; i<9; i++ )
    }
    else
    {
        Char msg3[30];
        StrPrintF( msg3, "Unknown Line Length %d", length );
        FrmCustomAlert( DebugAlert, msg3, "","" );
    }
   *lineP = line;
    return err;
}

/*
 * Add a Sudoku GameRecord to the Sudoku Database
 * by invoking the Sudoku App.
 */
Err addRecord( GameRecord* newRecord )
{
    Err err = errNone;
    LocalID sudokuId = DmFindDatabase( 0, "SudokuAGsu" );
    if ( sudokuId == 0 )
    {
        err = ERR_COULD_NOT_FIND_SUDOKU_APP;
        return err;
    }
    UInt32 result = 0;
    err = SysAppLaunch( 0, sudokuId, 0, sysAppLaunchCmdAddRecord, newRecord, &result );
    return err;
}

/*
 * Event handler for the main form.
 */
static Boolean mainFormEventHandler(EventPtr pEvent)
{
    Boolean handled = false;
    FormPtr pForm   = FrmGetActiveForm();
    switch (pEvent->eType)
    {
    case frmOpenEvent:    // Form's 1st event
        FrmDrawForm(pForm);
        mainFormInit(pForm);
        handled = true;
        break;
    case menuEvent:
        handled = doMainAction( pForm, pEvent->data.menu.itemID );
        break;
    case ctlSelectEvent:
        handled = doMainControl( pForm, pEvent->data.ctlSelect.controlID );
        break;
    case keyDownEvent:
        handled = doMainKey( pForm, pEvent->data.keyDown.chr );
        break;        
    // *** ADD EVENT HANDLING HERE *** //
    default:
        break;
    }
    return handled;
}

/*
 * This is the key handler for the main form.
 */
static Boolean doMainKey (FormPtr pForm, WChar chr)
{
    Boolean    handled    = false;
    ListType* listP = (ListType *)getObjectPtr( pForm, MemoList );
    if ( listP == NULL )
    {
        return handled;
    }
    Int16 item = LstGetSelection( listP );
    Int16 max = LstGetNumberOfItems( listP );
    switch( chr )
    {
    case pageUpChr:
        if( item > 0 )
        {
            item--;
        }
        LstSetSelection( listP, item );
        handled = true;
        break;
    case pageDownChr:
        if( item < max-1 )
        {
            item++;
        }
        LstSetSelection( listP, item );
        handled = true;
        break;
     case 310:
        doMainAction( pForm, ImportFromMemo );
        handled = true;
        break;
    default:
        {
        Char message[50];
        StrPrintF( message, "chrDown %d", chr );
        RectangleType rect;
        rect.topLeft.x = 4;
        rect.topLeft.y = 18;
        rect.extent.x = 154;
        rect.extent.y = 11;
        // WinEraseRectangle( &rect, 0 );
        // WinDrawChars (message,StrLen(message),4,18);
        }
        break;
    }
    return handled;
}

/*
 * This is the key handler for the main form.
 */
static Boolean doMainControl (FormPtr pForm, UInt16 ctl)
{
    Boolean    handled    = false;
    switch( ctl )
    {
    case MainFormImportButton:
        handled = doMainAction( pForm, ImportFromMemo );
        break;
    case CategoryTrigger:
        {
            Boolean categoryEdited;
            UInt16 category;
            categoryEdited = CategorySelect (memoDb, pForm,  
                CategoryTrigger, CategoryList, true, &category,  
                categoryName, 1, categoryDefaultEditCategoryString);
            if ( category != gPrefs.CurrentCategory )
            {
                gPrefs.CurrentCategory = category;
                updateList( pForm );
            }
        }
        handled = true;
        break;

    }
    return handled;
}

/*
 * This is the menu handler for the main form.
 */
static Boolean doMainAction(FormPtr pForm, UInt16 action)
{
    Boolean    handled    = false;
    switch(action)
    {
    case DisplayAbout:
        /* Get the version. */    
        MemHandle verH = DmGetResource( 'tver', 1000 );
        Char* ver = (Char*) MemHandleLock( verH ); 
        FrmCustomAlert( AboutAlert, ver, "","" );
        /* Unlock the resource */
        MemHandleUnlock( verH );
        DmReleaseResource( verH );
        break;
    case ImportFromMemo:
        Char message[50];
        message[0] = 0;
        if ( pForm == NULL )
        {
            StrPrintF( message, "Null Form!!!" );
        }
        else
        {
            ListType* listP = (ListType *)getObjectPtr( pForm, MemoList );
            if ( listP != NULL )
            {
                Int16 choice = LstGetSelection( listP );
                if ( choice == noListSelection )
                {
                    break;
                }
                Char *line = LstGetSelectionText( listP, choice );
                UInt16 *recIndex = (UInt16*)(&line[textSize]);

                // ListType * listP = (ListType *)getObjectPtr( pForm, MemoList );
                MemHandle recordH = DmQueryRecord( memoDb, *recIndex );
                MemPtr recordP = MemHandleLock( recordH );

                MemMove(&message[StrLen(message)], recordP,
                    49-StrLen(message) );
                message[49] = 0;
                Char* newline = StrChr( message, 10 );
                if ( newline != NULL )
                {
                    *newline = 0;
                }
                int puzzles = 0;
                Err err = processRecord( recordP, &puzzles );
                if ( err != errNone )
                {
                    StrPrintF( message, "Import Error %d", err );
                }
                else
                {
                     StrPrintF( message, "Imported %d Puzzles from Memo %d!", puzzles, choice );
                }
                err = MemHandleUnlock( recordH );
                recordH = NULL;
                recordP = NULL;
                if ( err != errNone )
                {
                    StrPrintF( message, "Unlock Error" );
                    break;
                }
           }
            else
            {
                StrPrintF( message, "GetList Error!");
            }
        }
        RectangleType rect;
        rect.topLeft.x = 4;
        rect.topLeft.y = 18;
        rect.extent.x = 154;
        rect.extent.y = 11;
        WinEraseRectangle( &rect, 0 );
        WinDrawChars (message,StrLen(message),4,18);
        break;
    }
    return handled;
}

static void updateList( FormPtr pForm )
{
    UInt16 i, recIndex=0;
    MemHandle recordH;
    MemPtr recordP;
    recordC = DmNumRecordsInCategory( memoDb, gPrefs.CurrentCategory );
    ListType * listP = (ListType *)getObjectPtr( pForm, MemoList );
    items = (Char **)MemPtrNew( recordC * sizeof(Char*));
    for ( i=0; i<recordC; i++ )
    {
        recordH = DmQueryNextInCategory ( memoDb, &recIndex, gPrefs.CurrentCategory );
        if ( recordH == NULL )
        {
            //message = "Query Error";
            items[i] = (Char *)MemPtrNew( 12 );
            //MemMove( items[i], message, 12 );
            //WinDrawChars (message,StrLen(message),20,18);
            continue;
        }
        recordP = MemHandleLock( recordH );
        items[i] = (Char *)MemPtrNew( textSize + 2);
        MemMove( items[i], recordP, textSize-2 );
        items[i][textSize-1] = 0;
        UInt16 *r =(UInt16*)(&items[i][textSize]);
        *r = recIndex;
        Char* newline = StrChr( items[i], 10 );
        if ( newline != NULL )
        {
            *newline = 0;
        }
        Err err = MemHandleUnlock( recordH );
        recordH = NULL;
        recordP = NULL;
        if ( err != errNone )
        {
            //message = "Get Error";
            //WinDrawChars (message,StrLen(message),20,18);
            break;
        }
        recIndex++;
    }
    LstSetListChoices( listP, items, recordC );
    LstDrawList( listP );
}

/*
 * Startup code for the main form.
 */
static void mainFormInit (FormPtr pForm)
{
    Char   * message    = "Hello GUI";
    updateList( pForm );

    UInt16 attr, category;
    ControlType *ctl; 

    // If current category is All, we need to look  
    // up category. 
    if ( gPrefs.CurrentCategory == dmAllCategories )
    { 
       DmRecordInfo( memoDb, 0, &attr, NULL, NULL);    
       category = attr & dmRecAttrCategoryMask; 
    }
    else
    {
       category = gPrefs.CurrentCategory; 
    }
    CategoryGetName ( memoDb, category, categoryName );
    ctl = FrmGetObjectPtr(pForm, FrmGetObjectIndex(pForm, CategoryTrigger)); 
    CategorySetTriggerLabel (ctl, categoryName); 
        {
        Char message[50];
        StrPrintF( message, "\"%s\"", categoryName );
        RectangleType rect;
        rect.topLeft.x = 4;
        rect.topLeft.y = 18;
        rect.extent.x = 154;
        rect.extent.y = 11;
        WinEraseRectangle( &rect, 0 );
        WinDrawChars (message,StrLen(message),4,18);
        }
    message    = "Hello GUI";
    WinDrawChars (message,StrLen(message),20,18);
}


// Utility Functions.

/*
 * Get a pointer to an object on a form, given its id.
 */
void * getObjectPtr (FormPtr pForm, Int16 resourceNo)
{
    UInt16 objIndex=FrmGetObjectIndex(pForm,resourceNo);
    return FrmGetObjectPtr(pForm,objIndex);
}

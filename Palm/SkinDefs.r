type 'Skin' {
	integer;					/* Skin version - must be 1 for this skin structure */
	cstring[24];			/* Skin name - can be 23 chars + zero at the end */
	integer NONE=1, SONY=2, HANDERA=4, HIGHDENSITY=8;/* High resolution mode */
	unsigned longint;		/* Minimal supported color depth */

	integer;					/* Title height */
	integer	NO=0, YES=1;/* Standard Palm OS title with time */
	integer;					/* Title bar bitmap ID */
	rect;						/* Title bar rectangle */

	integer;					/* Refresh button bitmap ID */
	integer;					/* Refresh button selected bitmap ID */
	rect;						/* Refresh button rectangle */

	integer;					/* Memory bitmap ID */
	rect;						/* Memory - the full size rectangle */
	rect;						/* Memory - bar display rectangle */
	integer;					/* Memory - delimiting vertical line color color */
	integer;					/* Memory - delimiting vertical line color gray */

	integer;					/* Battery bitmap ID */
	integer;					/* Battery charging bitmap ID */
	rect;						/* Battery - the full size rectangle */
	rect;						/* Battery - bar display rectangle */
	integer;					/* Battery - delimiting vertical line color color */
	integer;					/* Battery - delimiting vertical line color gray */
	
	integer;					/* Homer bitmap ID */
	integer;					/* Homer selected bitmap ID */
	rect;						/* Homer bitmap rectangle */
	rect;						/* Homer hot-spot rectangle */

	integer;					/* Gadget toggle bitmap ID */
	integer;					/* Gadget toggle selected bitmap ID */
	rect;						/* Gadget toggle bitmap rectangle */
	rect;						/* Gadget toggle hot-spot rectangle */

	integer;					/* Gadget bar background bitmap ID */
	rect;						/* Gadget bar background rectangle */

	integer;					/* Number of visible gadgets (max is 16) */
	integer	NO=0, YES=1;/* Gadgets vertical */
	point;					/* starting point for drawing gadgets */
	integer;					/* gadget horizontal padding */
	integer;					/* gadget width */
	integer;					/* gadget height */
	
	integer;					/* Number of gadgets */
	integer;					/* First gadget bitmap ID */
	integer;					/* First gadget selected bitmap ID */
	
	Integer;					/* GadgetLockUnlock bitmapID */
	Integer;					/* GadgetLockUnlock selected bitmapID */
	
	rect;						/* App area - gadgets hidden*/
	rect;						/* App area - gadgets drawn*/
	
	integer DEFAULT=0, RIGHT=1, LEFT=2;	/* Scrollbar position */
	integer;					/* Scrollbar width */
	integer;					/* Scrollbar background color color */
	integer;					/* Scrollbar background color gray */
	integer;					/* Scrollbar foreground color color */
	integer;					/* Scrollbar foreground color gray */
	integer;					/* Scrollbar vertical size correction */
	
	integer;					/* Number of category icons */
	integer;					/* First category icon bitmap ID */
	integer;					/* Category icon width */
	integer;					/* Category icon height */
	
	integer NONE=0, UP=1, LEFT=2, RIGHT=3;	/* Tabs position */
	integer NO=0, YES=1;	/* Two rows of tabs */
	integer;					/* Bitmap ID of the slice: left */
	integer;					/* Bitmap ID of the slice: selected left */
	integer;					/* Bitmap ID of the slice: selected right */
	integer;					/* Bitmap ID of the slice: right - last tab*/	
	integer;					/* Bitmap ID of the slice: left after selected */
	integer;					/* Bitmap ID of the slice: right - non-last tab */

	integer;					/* Slice height */
	integer;					/* Slice width */
	integer;					/* Upper line thickness */
	integer;					/* Non-selected real height */
	
	integer;					/* Bitmap ID of the "Previous tab" scroll arrow */
	integer;					/* Bitmap ID of the "Next tab" scroll arrow */
	integer;					/* Tab scroll arrow height */
	integer;					/* Tab scroll arrow width */
	
	integer;					/* horizontal offset from the left side of the left slice */
	integer;					/* horizontal offset from the left side of the "afer selected" slice */
	integer;					/* horizontal offset from the right side of the right slice */
	integer;					/* horizontal offset from the right side of the "before selected" slice */
	integer;					/* vertical offset from the top of the slice */
	integer;					/* vertical offset from the top of the selected slice */

	rect;						/* App area to be painted with the background color */

	};


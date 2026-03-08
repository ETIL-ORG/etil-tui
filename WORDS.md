<!--
Copyright (c) 2026 Mark Deazley. All rights reserved.
SPDX-License-Identifier: BSD-3-Clause
-->

# ETIL Word Reference — v0.8.13

Complete reference for all built-in words in the Evolutionary Threaded Interpretive Language (ETIL).
Words are organized by category. Stack effects use FORTH notation: `( inputs -- outputs )`.

## Quick Links

| # | Category | Words | Link |
|---|----------|------:|------|
| 1 | Arithmetic | 12 | [Arithmetic](#arithmetic) |
| 2 | Stack | 12 | [Stack](#stack) |
| 3 | Comparison | 9 | [Comparison](#comparison) |
| 4 | Logic | 11 | [Logic](#logic) |
| 5 | I/O | 8 | [I/O](#io) |
| 6 | Memory | 8 | [Memory](#memory) |
| 7 | Math | 24 | [Math](#math) |
| 8 | String | 19 | [String](#string) |
| 9 | Array | 10 | [Array](#array) |
| 10 | ByteArray | 7 | [ByteArray](#bytearray) |
| 11 | Map | 8 | [Map](#map) |
| 12 | JSON | 13 | [JSON](#json) |
| 13 | LVFS | 6 | [LVFS](#lvfs) |
| 14 | System | 6 | [System](#system) |
| 15 | Time | 12 | [Time](#time) |
| 16 | Input Reading | 2 | [Input Reading](#input-reading) |
| 17 | Dictionary Ops | 10 | [Dictionary Ops](#dictionary-ops) |
| 18 | Metadata Ops | 12 | [Metadata Ops](#metadata-ops) |
| 19 | Help | 1 | [Help](#help) |
| 20 | Execution | 5 | [Execution](#execution) |
| 21 | Conversion | 5 | [Conversion](#conversion) |
| 22 | Debug | 4 | [Debug](#debug) |
| 23 | File I/O (async) | 13 | [File I/O (async)](#file-io-async) |
| 24 | File I/O (sync) | 13 | [File I/O (sync)](#file-io-sync) |
| 25 | HTTP Client | 2 | [HTTP Client](#http-client) |
| 26 | MongoDB | 5 | [MongoDB](#mongodb) |
| 27 | Matrix | 25 | [Matrix](#matrix) |
| 28 | Parsing | 3 | [Parsing](#parsing) |
| 29 | Self-hosted | 8 | [Self-hosted](#self-hosted) |
| 30 | Control Flow | 20 | [Control Flow](#control-flow) |
|   | **Total** | **283** | |

---

## Arithmetic

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `+` | `( a b -- a+b )` | Add two numbers |
| `-` | `( a b -- a-b )` | Subtract top from second |
| `*` | `( a b -- a*b )` | Multiply two numbers |
| `/` | `( a b -- a/b )` | Divide second by top (truncating for integers) |
| `mod` | `( a b -- a%b )` | Remainder of second divided by top |
| `/mod` | `( a b -- rem quot )` | Divide with remainder |
| `negate` | `( n -- -n )` | Negate top of stack |
| `abs` | `( n -- \|n\| )` | Absolute value of top of stack |
| `max` | `( n1 n2 -- max )` | Return the greater of two values |
| `min` | `( n1 n2 -- min )` | Return the lesser of two values |
| `1+` | `( n -- n+1 )` | Increment by one |
| `1-` | `( n -- n-1 )` | Decrement by one |

## Stack

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `dup` | `( x -- x x )` | Duplicate top of stack |
| `drop` | `( x -- )` | Remove top of stack |
| `swap` | `( a b -- b a )` | Swap top two stack items |
| `over` | `( a b -- a b a )` | Copy second item to top |
| `rot` | `( a b c -- b c a )` | Rotate third item to top |
| `-rot` | `( a b c -- c a b )` | Reverse rotate: move TOS under third item |
| `pick` | `( xn ... x1 x0 n -- xn ... x1 x0 xn )` | Copy the Nth item (zero-based) below TOS onto TOS |
| `nip` | `( x1 x2 -- x2 )` | Remove second item, keeping TOS |
| `tuck` | `( x1 x2 -- x2 x1 x2 )` | Copy TOS under second item |
| `depth` | `( -- u )` | Push current data stack depth |
| `?dup` | `( x -- x x \| 0 )` | Duplicate TOS if non-zero |
| `roll` | `( xu ... x0 u -- xu-1 ... x0 xu )` | Move the Nth item (zero-based) to TOS, removing it from its original position |

## Comparison

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `=` | `( a b -- bool )` | Test equality |
| `<>` | `( a b -- bool )` | Test inequality |
| `<` | `( a b -- bool )` | Test less than |
| `>` | `( a b -- bool )` | Test greater than |
| `<=` | `( a b -- bool )` | Test less than or equal |
| `>=` | `( a b -- bool )` | Test greater than or equal |
| `0=` | `( n -- bool )` | Test if zero |
| `0<` | `( n -- bool )` | Test if negative |
| `0>` | `( n -- bool )` | Test if positive |

## Logic

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `true` | `( -- bool )` | Push boolean true onto the stack |
| `false` | `( -- bool )` | Push boolean false onto the stack |
| `not` | `( x -- bool )` | Logical negation. Boolean: logical NOT. Integer: 0= coerced to Boolean. Float: 0.0= coerced to Boolean |
| `and` | `( a b -- a&b )` | Both Boolean: logical AND. Both Integer: bitwise AND. Mixed types: error |
| `or` | `( a b -- a\|b )` | Both Boolean: logical OR. Both Integer: bitwise OR. Mixed types: error |
| `xor` | `( a b -- a^b )` | Both Boolean: logical XOR. Both Integer: bitwise XOR. Mixed types: error |
| `invert` | `( n -- ~n )` | Boolean: logical NOT. Integer: bitwise NOT |
| `lshift` | `( x u -- x<<u )` | Left bit shift |
| `rshift` | `( x u -- x>>u )` | Logical right bit shift |
| `lroll` | `( x u -- x' )` | Bitwise rotate left (circular shift) |
| `rroll` | `( x u -- x' )` | Bitwise rotate right (circular shift) |

## I/O

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `.` | `( x -- )` | Print and consume top of stack |
| `cr` | `( -- )` | Print newline |
| `emit` | `( char -- )` | Print character from ASCII code |
| `space` | `( -- )` | Print a space |
| `spaces` | `( n -- )` | Print n spaces |
| `words` | `( -- )` | List all dictionary words |
| `."` | `( -- )` | Print string literal (interpret/compile) |
| `.\|` | `( -- )` | Print string literal with escape processing |

## Memory

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `create` | `( -- )` | Define a new word with a data field |
| `,` | `( x -- )` | Append value to last created word's data field |
| `@` | `( dataref -- x )` | Fetch value from bounds-checked DataRef |
| `!` | `( x dataref -- )` | Store value via bounds-checked DataRef |
| `allot` | `( n -- )` | Reserve n cells in last created word |
| `variable` | `( -- )` | Define a new variable initialized to zero |
| `constant` | `( x -- )` | Define a named constant |
| `immediate` | `( -- )` | Mark the most recently defined word as immediate (executed during compilation) |

## Math

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `sqrt` | `( x -- sqrt(x) )` | Square root |
| `sin` | `( x -- sin(x) )` | Sine (radians) |
| `cos` | `( x -- cos(x) )` | Cosine (radians) |
| `tan` | `( x -- tan(x) )` | Tangent (radians) |
| `asin` | `( x -- asin(x) )` | Arc sine |
| `acos` | `( x -- acos(x) )` | Arc cosine |
| `atan` | `( x -- atan(x) )` | Arc tangent |
| `atan2` | `( y x -- atan2(y,x) )` | Two-argument arc tangent |
| `log` | `( x -- ln(x) )` | Natural logarithm |
| `log2` | `( x -- log2(x) )` | Base-2 logarithm |
| `log10` | `( x -- log10(x) )` | Base-10 logarithm |
| `exp` | `( x -- e^x )` | Exponential (e^x) |
| `pow` | `( base exp -- base^exp )` | Raise base to exponent |
| `ceil` | `( x -- ceil(x) )` | Ceiling (round up) |
| `floor` | `( x -- floor(x) )` | Floor (round down) |
| `round` | `( x -- round(x) )` | Round to nearest integer |
| `trunc` | `( r -- r )` | Truncate toward zero (FORTH FTRUNC) |
| `fmin` | `( a b -- min(a,b) )` | Minimum of two numbers |
| `fmax` | `( a b -- max(a,b) )` | Maximum of two numbers |
| `pi` | `( -- pi )` | Push pi (3.14159...) |
| `f~` | `( r1 r2 r3 -- flag )` | Approximate float equality (FORTH F~). r3>0: absolute tolerance. r3=0: exact equality. r3<0: relative tolerance |
| `random` | `( -- f )` | Push a pseudo-random float in [0.0, 1.0) |
| `random-seed` | `( n -- )` | Seed the PRNG engine (same seed produces same sequence) |
| `random-range` | `( lo hi -- n )` | Push a pseudo-random integer in [lo, hi) |

## String

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `s"` | `( -- str )` | Create heap string literal (interpret/compile) |
| `s\|` | `( -- str )` | Push string literal with escape processing |
| `type` | `( str -- )` | Print a heap string |
| `s+` | `( str1 str2 -- str3 )` | Concatenate two strings |
| `s=` | `( str1 str2 -- bool )` | Test string equality |
| `s<>` | `( str1 str2 -- bool )` | Test string inequality |
| `slength` | `( str -- n )` | Get string length in bytes |
| `substr` | `( str start len -- substr )` | Extract substring |
| `strim` | `( str -- trimmed )` | Trim whitespace from both ends |
| `sfind` | `( str needle -- index )` | Find substring, return index or -1 |
| `sreplace` | `( str old new -- result )` | Replace all occurrences of substring |
| `ssplit` | `( str delim -- array )` | Split string by delimiter into array |
| `sjoin` | `( array delim -- str )` | Join array of strings with delimiter |
| `sregex-find` | `( str pattern -- match flag )` | Find first regex match |
| `sregex-replace` | `( str pattern replacement -- result )` | Replace regex matches |
| `sregex-search` | `( str pattern -- match-array -1 \| 0 )` | Find first regex match anywhere in string, returning capture groups as array |
| `sregex-match` | `( str pattern -- match-array -1 \| 0 )` | Test if entire string matches regex pattern, returning capture groups as array |
| `sprintf` | `( arg1 ... argN fmt -- string )` | C-style formatted string (supports %d %f %s %x %o %e %g %c %%) |
| `staint` | `( string -- bool )` | Query whether a string is tainted (originated from external I/O) |

## Array

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `array-new` | `( -- array )` | Create a new empty array |
| `array-push` | `( array value -- array )` | Push value onto end of array |
| `array-pop` | `( array -- array value )` | Pop value from end of array |
| `array-get` | `( array index -- value )` | Get value at index |
| `array-set` | `( array index value -- array )` | Set value at index |
| `array-length` | `( array -- array n )` | Get number of elements |
| `array-shift` | `( array -- array value )` | Remove and return first element |
| `array-unshift` | `( array value -- array )` | Insert value at beginning |
| `array-compact` | `( array -- array )` | Remove zero/null elements |
| `array-reverse` | `( array -- array )` | Reverse array in-place |

## ByteArray

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `bytes-new` | `( n -- bytes )` | Create a new byte array of given size |
| `bytes-get` | `( bytes index -- value )` | Get byte at index |
| `bytes-set` | `( bytes index value -- bytes )` | Set byte at index |
| `bytes-length` | `( bytes -- n )` | Get byte array length |
| `bytes-resize` | `( bytes n -- bytes )` | Resize byte array |
| `bytes->string` | `( bytes -- str )` | Convert byte array to string |
| `string->bytes` | `( str -- bytes )` | Convert string to byte array |

## Map

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `map-new` | `( -- map )` | Create an empty hash map |
| `map-set` | `( map key val -- map )` | Set key (string) to value, return map |
| `map-get` | `( map key -- val )` | Get value by key; fails if key not found |
| `map-remove` | `( map key -- map )` | Remove key from map; fails if key not found |
| `map-length` | `( map -- n )` | Push the number of entries in the map |
| `map-keys` | `( map -- arr )` | Push an array of all keys (strings) |
| `map-values` | `( map -- arr )` | Push an array of all values |
| `map-has?` | `( map key -- bool )` | Test if key exists in map |

## JSON

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `j\|` | `j\| ... \| ( -- json )` | JSON literal handler word: parse text to closing \| as JSON |
| `json-parse` | `( string -- json )` | Parse a JSON string into a HeapJson value |
| `json-dump` | `( json -- string )` | Convert JSON value to compact string |
| `json-pretty` | `( json -- string )` | Convert JSON value to indented string |
| `json-get` | `( json key\|index -- value )` | Look up by string key in JSON object or integer index in JSON array; nested objects stay as JSON |
| `json-length` | `( json -- int )` | Array length or object size |
| `json-type` | `( json -- string )` | Type of JSON value: object, array, string, number, boolean, null |
| `json-keys` | `( json -- array )` | Get array of object keys as strings |
| `json->map` | `( json -- map )` | Recursively convert JSON object to HeapMap |
| `json->array` | `( json -- array )` | Recursively convert JSON array to HeapArray |
| `map->json` | `( map -- json )` | Recursively convert HeapMap to JSON object |
| `array->json` | `( array -- json )` | Recursively convert HeapArray to JSON array |
| `json->value` | `( json -- value )` | Auto-unpack JSON: object->map, array->array, string->string, number->int/float, boolean->bool |

## LVFS

The Little Virtual File System provides navigation and file viewing within the sandboxed `/home` (writable) and `/library` (read-only) directories.

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `cwd` | `( -- )` | Print current working directory (virtual path) |
| `cd` | `( -- )` | Change working directory. No argument resets to /home. Accepts absolute (/library) or relative (sub) virtual paths |
| `ls` | `( -- )` | List directory contents. No argument lists CWD. Directories shown with trailing / |
| `ll` | `( -- )` | Long-format directory listing sorted by modification time (newest first). Shows size, date, and name |
| `lr` | `( -- )` | Recursive long-format directory listing sorted by modification time (newest first). Shows relative paths |
| `cat` | `( -- )` | Print the contents of a file. Requires a file path argument |

## System

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `sys-semver` | `( -- )` | Print project semantic version |
| `sys-timestamp` | `( -- )` | Print build timestamp |
| `sys-datafields` | `( -- )` | Print DataFieldRegistry diagnostics (entries, live, cells, bytes) |
| `sys-notification` | `( x -- )` | Queue a MCP notification (any value auto-converted to string). Requires send_system_notification permission |
| `user-notification` | `( msg-str user-id-str -- flag )` | Send a notification to all sessions of a specific user. Requires send_user_notification permission |
| `abort` | `( flag -- ) or ( error-string false -- )` | Terminate interpretation. With true flag: success abort. With false flag: pops error message, error abort |

## Time

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `time-us` | `( -- n )` | Push current UTC time as microseconds since epoch (int64) |
| `us->iso` | `( n -- str )` | Format microseconds as compact ISO 8601 string (YYYYMMDDTHHMMSSZ) |
| `us->iso-us` | `( n -- str )` | Format microseconds as high-res ISO 8601 string (YYYYMMDDTHHMMSS.ddddddZ) |
| `time-iso` | `( -- str )` | Push current UTC time as compact ISO 8601 string |
| `time-iso-us` | `( -- str )` | Push current UTC time as high-res ISO 8601 string with microseconds |
| `us->jd` | `( n -- f )` | Convert UTC microseconds since epoch to Julian Date |
| `jd->us` | `( f -- n )` | Convert Julian Date to UTC microseconds since epoch |
| `us->mjd` | `( n -- f )` | Convert UTC microseconds since epoch to Modified Julian Date |
| `mjd->us` | `( f -- n )` | Convert Modified Julian Date to UTC microseconds since epoch |
| `time-jd` | `( -- f )` | Push current UTC time as Julian Date |
| `time-mjd` | `( -- f )` | Push current UTC time as Modified Julian Date |
| `sleep` | `( n -- )` | Sleep for the given number of microseconds. Errors if the duration would exceed the execution deadline |

## Input Reading

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `word-read` | `( -- str flag )` | Read next whitespace-delimited token |
| `string-read-delim` | `( char -- str flag )` | Read string between delimiters |

## Dictionary Ops

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `dict-forget` | `( name-str -- flag )` | Remove latest implementation of word |
| `dict-forget-all` | `( name-str -- flag )` | Remove all implementations of word |
| `file-load` | `( path-str -- flag )` | Load and interpret a TIL file |
| `include` | `( -- )` | Load a TIL file (reads path from input) |
| `library` | `( -- )` | Load a TIL file from the library directory (reads path from input) |
| `evaluate` | `( str -- )` | Interpret a string as TIL code at runtime. Tracks call depth for recursion safety |
| `marker` | `( -- )` | Create a dictionary checkpoint (FORTH MARKER). Executing the marker word later restores the dictionary to the state before the marker was created |
| `marker-restore` | `( name-str -- )` | Restore dictionary to a marker checkpoint (internal helper) |
| `forget` | `( -- )` | Remove latest implementation of a word (self-hosted, reads name from input) |
| `forget-all` | `( -- )` | Remove all implementations of a word (self-hosted, reads name from input) |

## Metadata Ops

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `dict-meta-set` | `( word-str key-str fmt-str content-str -- flag )` | Set concept-level metadata |
| `dict-meta-get` | `( word-str key-str -- content-str flag )` | Get concept-level metadata |
| `dict-meta-del` | `( word-str key-str -- flag )` | Delete concept-level metadata entry |
| `dict-meta-keys` | `( word-str -- array flag )` | List concept-level metadata keys |
| `impl-meta-set` | `( word-str key-str fmt-str content-str -- flag )` | Set implementation-level metadata |
| `impl-meta-get` | `( word-str key-str -- content-str flag )` | Get implementation-level metadata |
| `meta!` | `( word-str key-str fmt-str content-str -- flag )` | Set concept-level metadata (self-hosted alias) |
| `meta@` | `( word-str key-str -- content-str flag )` | Get concept-level metadata (self-hosted alias) |
| `meta-del` | `( word-str key-str -- flag )` | Delete concept-level metadata (self-hosted alias) |
| `meta-keys` | `( word-str -- array flag )` | List metadata keys for a word (self-hosted alias) |
| `impl-meta!` | `( word-str key-str fmt-str content-str -- flag )` | Set implementation-level metadata (self-hosted alias) |
| `impl-meta@` | `( word-str key-str -- content-str flag )` | Get implementation-level metadata (self-hosted alias) |

## Help

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `help` | `( -- )` | Show help for a word (parsing word, reads name from input) |

## Execution

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `'` | `( -- xt )` | Parse next token, look up in dictionary, push execution token |
| `execute` | `( xt -- )` | Pop execution token and execute the referenced word |
| `xt?` | `( val -- bool )` | Test if TOS is an execution token |
| `>name` | `( xt -- str )` | Extract the word name from an execution token as a string |
| `xt-body` | `( xt -- dataref )` | Get data field reference from an execution token of a CREATE'd word |

## Conversion

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `bool` | `( x -- bool )` | Convert to boolean. Integer/Float: nonzero becomes true, zero becomes false. Boolean: pass-through |
| `int->float` | `( n -- f )` | Convert integer to float. Pass through if already float |
| `float->int` | `( f -- n )` | Convert float to integer (truncates toward zero). Pass through if already integer |
| `number->string` | `( n -- str )` | Convert a number (integer or float) to its string representation |
| `string->number` | `( str -- value -1 \| 0 )` | Parse a string as a number. On success push value and -1 (true). On failure push 0 (false) |

## Debug

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `dump` | `( x -- x )` | Deep-inspect top of stack (non-destructive) |
| `see` | `( -- )` | Decompile a word definition |
| `.s` | `( -- )` | Display the entire data stack without modifying it |
| `s.` | `( str -- )` | Print string with trailing space |

## File I/O (async)

Asynchronous file I/O using libuv's thread pool with cooperative await via `tick()`. All paths are virtual (`/home`, `/library`).

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `exists?` | `( path -- flag )` | Check if a file or directory exists at the given virtual path |
| `read-file` | `( path -- string? flag )` | Read entire file contents as a string. Works with /home and /library paths |
| `write-file` | `( string path -- flag )` | Write string to file, truncating any existing content. Only writes to /home |
| `append-file` | `( string path -- flag )` | Append string to file. Creates file if it does not exist. Only writes to /home |
| `copy-file` | `( src dest -- flag )` | Copy a file. Source can be /library, destination must be under /home |
| `rename-file` | `( old new -- flag )` | Rename or move a file/directory. Both paths must be under /home |
| `lstat` | `( path -- array? flag )` | Get file status as a 4-element array: [size, mtime_us, is_dir, is_read_only] |
| `readdir` | `( path -- array? flag )` | List directory contents as an array of filename strings |
| `mkdir` | `( path -- flag )` | Create a directory (and parents) under /home |
| `mkdir-tmp` | `( prefix -- string? flag )` | Create a unique temporary directory under /home with the given prefix. Returns virtual path |
| `rmdir` | `( path -- flag )` | Remove an empty directory under /home |
| `rm` | `( path -- flag )` | Remove a file or directory recursively under /home. Refuses to delete /home itself |
| `truncate` | `( path -- flag )` | Truncate a file to zero length. File must exist under /home |

## File I/O (sync)

Synchronous file I/O using libuv in blocking mode. Same behavior as async counterparts but blocking.

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `exists-sync` | `( path -- flag )` | Check if a file or directory exists at the given virtual path |
| `read-file-sync` | `( path -- string? flag )` | Read entire file contents as a string. Works with /home and /library paths |
| `write-file-sync` | `( string path -- flag )` | Write string to file, truncating any existing content. Only writes to /home |
| `append-file-sync` | `( string path -- flag )` | Append string to file. Creates file if it does not exist. Only writes to /home |
| `copy-file-sync` | `( src dest -- flag )` | Copy a file. Source can be /library (read-only), destination must be under /home |
| `rename-sync` | `( old new -- flag )` | Rename or move a file/directory. Both old and new paths must be under /home |
| `lstat-sync` | `( path -- array? flag )` | Get file status as a 4-element array: [size, mtime_us, is_dir, is_read_only] |
| `readdir-sync` | `( path -- array? flag )` | List directory contents as an array of filename strings |
| `mkdir-sync` | `( path -- flag )` | Create a directory (and parents) under /home |
| `mkdir-tmp-sync` | `( prefix -- string? flag )` | Create a unique temporary directory under /home with the given prefix. Returns virtual path |
| `rmdir-sync` | `( path -- flag )` | Remove an empty directory under /home |
| `rm-sync` | `( path -- flag )` | Remove a file or directory recursively under /home. Refuses to delete /home itself |
| `truncate-sync` | `( path -- flag )` | Truncate a file to zero length. File must exist under /home |

## HTTP Client

Outbound HTTP/HTTPS requests with SSRF protection, domain allowlist, and per-session fetch budgets. Domain must be in `ETIL_HTTP_ALLOWLIST`. SSRF protection blocks loopback, RFC1918, link-local, and cloud metadata IPs.

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `http-get` | `( url headers-map -- bytes status-code flag )` | Perform an HTTP/HTTPS GET request with extra headers. The headers parameter is a HeapMap of string key-value pairs (use `map-new` for no extra headers). Returns response body as opaque bytes (HeapByteArray), HTTP status code, and success flag |
| `http-post` | `( url headers-map body-bytes -- bytes status-code flag )` | Perform an HTTP/HTTPS POST request. Body is a HeapByteArray (use `string->bytes` to convert). Returns response body as opaque bytes, HTTP status code, and success flag |

## MongoDB

All MongoDB words require `mongo_access` permission. Filter, document, and options parameters accept String, Json, or Map types.

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `mongo-find` | `( coll filter opts -- json flag )` | Query a MongoDB collection. Options supports: skip, limit, sort, projection, hint, collation, max_time_ms, batch_size. Returns matching documents as a Json value. Results are tainted (external data) |
| `mongo-count` | `( coll filter opts -- count flag )` | Count documents in a MongoDB collection. Uses server-side count_documents(). Options supports: skip, limit, hint, collation, max_time_ms |
| `mongo-insert` | `( coll doc -- inserted-id flag )` | Insert a document into a MongoDB collection. Returns the inserted document _id as a string |
| `mongo-update` | `( coll filter update opts -- count flag )` | Update documents in a MongoDB collection. The update should use MongoDB update operators ($set, $inc, etc.). Options supports: upsert, hint, collation |
| `mongo-delete` | `( coll filter opts -- count flag )` | Delete documents from a MongoDB collection. Options supports: hint, collation. Returns count of deleted documents |

## Matrix

Linear algebra operations backed by LAPACK/BLAS routines. Available when built with `ETIL_BUILD_LINALG=ON` (default).

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `mat-new` | `( rows cols -- mat )` | Create a zero-filled matrix |
| `mat-eye` | `( n -- mat )` | Create an n x n identity matrix |
| `mat-from-array` | `( array rows cols -- mat )` | Create matrix from flat array (row-major order) |
| `mat-diag` | `( array -- mat )` | Create diagonal matrix from array of values |
| `mat-rand` | `( rows cols -- mat )` | Create matrix with random values in [0,1) |
| `mat-get` | `( mat row col -- val )` | Get matrix element (bounds-checked) |
| `mat-set` | `( mat row col val -- mat )` | Set matrix element (returns mat for chaining) |
| `mat-rows` | `( mat -- n )` | Get row count of matrix |
| `mat-cols` | `( mat -- n )` | Get column count of matrix |
| `mat-row` | `( mat i -- array )` | Extract row as HeapArray |
| `mat-col` | `( mat j -- array )` | Extract column as HeapArray |
| `mat*` | `( mat1 mat2 -- mat )` | Matrix multiply (DGEMM) |
| `mat+` | `( mat1 mat2 -- mat )` | Element-wise matrix addition |
| `mat-` | `( mat1 mat2 -- mat )` | Element-wise matrix subtraction |
| `mat-scale` | `( mat scalar -- mat )` | Multiply matrix by scalar |
| `mat-transpose` | `( mat -- mat )` | Transpose matrix |
| `mat-solve` | `( A b -- x flag )` | Solve Ax=b via LU factorization (DGESV). Flag 0=success |
| `mat-inv` | `( mat -- inv flag )` | Matrix inverse via LU (DGETRF+DGETRI). Flag 0=success |
| `mat-det` | `( mat -- det flag )` | Matrix determinant via LU factorization. Flag 0=success |
| `mat-eigen` | `( mat -- eigenvalues eigenvectors flag )` | Eigendecomposition (DSYEV for symmetric, DGEEV for general) |
| `mat-svd` | `( mat -- U S Vt flag )` | Singular value decomposition (DGESVD) |
| `mat-lstsq` | `( A b -- x flag )` | Least squares solve (DGELS) |
| `mat-norm` | `( mat -- val )` | Frobenius norm of matrix |
| `mat-trace` | `( mat -- val )` | Sum of diagonal elements (square matrix required) |
| `mat.` | `( mat -- )` | Pretty-print matrix (consumes it) |

## Parsing

Handler words processed by the outer interpreter.

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `:` | `( -- )` | Begin colon definition (interpret-only) |
| `;` | `( -- )` | End colon definition (compile-only) |
| `does>` | `( -- )` | Set runtime behavior for CREATE'd words (compile-only) |

## Self-hosted

Words defined in `data/builtins.til`, implemented in ETIL source.

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `variable` | `( -- )` | Define a new variable initialized to zero |
| `constant` | `( x -- )` | Define a named constant |
| `forget` | `( -- )` | Remove latest implementation of a word |
| `forget-all` | `( -- )` | Remove all implementations of a word |
| `meta!` | `( word-str key-str fmt-str content-str -- flag )` | Set concept-level metadata |
| `meta@` | `( word-str key-str -- content-str flag )` | Get concept-level metadata |
| `meta-del` | `( word-str key-str -- flag )` | Delete concept-level metadata |
| `meta-keys` | `( word-str -- array flag )` | List metadata keys for a word |

## Control Flow

All control flow words are **compile-only** -- they can only be used inside colon definitions (`: name ... ;`).

| Word | Stack Effect | Description |
|------|-------------|-------------|
| `if` | `( bool -- )` | Conditional branch. Requires Boolean on TOS |
| `else` | `( -- )` | Alternative branch |
| `then` | `( -- )` | End conditional |
| `do` | `( limit start -- )` | Begin counted loop |
| `loop` | `( -- )` | Increment and loop |
| `+loop` | `( n -- )` | Add increment and loop |
| `i` | `( -- n )` | Push current loop index |
| `j` | `( -- n )` | Push outer loop index |
| `begin` | `( -- )` | Begin indefinite loop |
| `until` | `( bool -- )` | Loop until true. Requires Boolean on TOS |
| `while` | `( bool -- )` | Test and continue loop. Requires Boolean on TOS |
| `repeat` | `( -- )` | End begin/while loop |
| `again` | `( -- )` | Unconditional loop back to begin |
| `>r` | `( x -- ) ( R: -- x )` | Move value to return stack |
| `r>` | `( -- x ) ( R: x -- )` | Move value from return stack |
| `r@` | `( -- x ) ( R: x -- x )` | Copy top of return stack |
| `leave` | `( -- )` | Exit do loop immediately |
| `exit` | `( -- )` | Return from current word |
| `recurse` | `( -- )` | Call current word recursively |
| `[']` | `( -- xt )` | Compile-time tick -- push xt at runtime |

---

> **Note:** This document should be kept in sync with `data/help.til` in the
> [ETIL repository](https://github.com/krystalmonolith/evolutionary-til)
> when words are added or changed.

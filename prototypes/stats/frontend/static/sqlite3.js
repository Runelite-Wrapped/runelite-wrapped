window.sqlite3InitModule().then(function (sqlite3) {
    // The module is now loaded and the sqlite3 namespace
    // object was passed to this function.
    console.log("sqlite3:", sqlite3);
});

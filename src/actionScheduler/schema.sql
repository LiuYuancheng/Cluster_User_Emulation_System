DROP TABLE IF EXISTS dailyActions;

CREATE TABLE dailyActions (
    actId INTEGER PRIMARY KEY NOT NULL,
    actName TEXT NOT NULL,
    actDetail TEXT,
    actDesc TEXT,
    actOwner TEXT,
    actType INTEGER NOT NULL DEFAULT 1, 
    startT TEXT NOT NULL,
    depend INTEGER DEFAULT 0,
    threadType INTEGER NOT NULL DEFAULT 1,
    actState TEXT NOT NULL,
    nextT TEXT NOT NULL
);
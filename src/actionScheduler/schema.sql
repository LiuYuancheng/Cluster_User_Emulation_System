DROP TABLE IF EXISTS dailyActions;
DROP TABLE IF EXISTS randomActions;
DROP TABLE IF EXISTS weeklyActions;

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

CREATE TABLE randomActions (
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

CREATE TABLE weeklyActions (
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

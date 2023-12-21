package com.tracker;

public class DbClientFactory {
    public DbClient createDbClient(String dbString) {
        return new DbClient(dbString);
    }
}

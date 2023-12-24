package com.tracker;

import java.util.Map;
import java.util.HashMap;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.tracker.models.TelemetryData;

// this is for sqlite
public class DbClient {
    private String dbString;
    private Map<String, String> eventToTable = createMap();

    private static Map<String, String> createMap() {
        Map<String, String> eventToTable = new HashMap<String, String>();
        eventToTable.put("stat-changed", "stat_changed");
        eventToTable.put("hitsplat-applied", "hitsplat_applied");
        eventToTable.put("actor-death", "actor_death");
        eventToTable.put("grand-exchange-offer-changed", "grand_exchange_offer_changed");
        eventToTable.put("game-tick", "game_tick");
        eventToTable.put("loot-received", "loot_received");
        return eventToTable;
    }

    private String getCreateTableQuery(String table) {
        // each table has an id column and a TEXT column (will just be json)
        String query = "CREATE TABLE IF NOT EXISTS " + table + " (\n" + "id integer PRIMARY KEY,\n"
                + "data text NOT NULL\n" + ");";

        return query;
    }

    public void initialiseDb() {

        Connection con = connect();

        // create a table for each event
        for (String event : eventToTable.keySet()) {
            String table = eventToTable.get(event);
            String query = getCreateTableQuery(table);
            try {
                con.createStatement().execute(query);
            } catch (Exception e) {
                System.out.println(e.getMessage());
            }
        }

        try {
            con.commit();
            con.close();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    public void StoreTelemetry(TelemetryData telemetryData) {
        Connection con = connect();
        String table = eventToTable.get(telemetryData.getEvent());

        if (table == null) {
            System.out.println("No table found for event: " + telemetryData.getEvent());
            return;
        }

        String query = "INSERT INTO " + table + " (data) VALUES (?);";

        ObjectMapper mapper = new ObjectMapper();
        try {
            String json = mapper.writeValueAsString(telemetryData);
            PreparedStatement stmt = con.prepareStatement(query);
            stmt.setString(1, json);
            stmt.executeUpdate();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }

        try {
            con.commit();
            con.close();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    public Connection connect() {

        // TODO: actually put some thought into connection management
        Connection conn = null;
        try {
            // check if the appropriate class is available
            Class.forName("org.sqlite.JDBC");
            conn = DriverManager.getConnection(dbString);
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        return conn;
    }

    // constructor
    public DbClient(String dbString) {
        // prefix with jdbc:sqlite:
        this.dbString = "jdbc:sqlite:" + dbString;
    }
}

package com.tracker.models;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

// telemetry data class definition
@Getter
@RequiredArgsConstructor
public class TelemetryData {
    private final long timestamp;
    private final Object data;
    private final String username;
    private final String event;
    private final long tickCount;
    private final String sessionId;
}

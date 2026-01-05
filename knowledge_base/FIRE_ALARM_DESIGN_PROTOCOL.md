# Fire Alarm System Design Protocol (Florida Jurisdiction)

**Author**: Licensed Professional Engineer (Fire Protection)
**Date**: 2026-01-04
**Jurisdiction**: Florida (Statewide)

---

## Phase 1: Architectural Plan Review
**Objective**: Extract critical building parameters to determine the "Risk Profile" and "System Type".

### 1.1 Occupancy Classification (The Foundation)
*Ref: NFPA 101 / FBC Building Ch. 3*
I first verify the **Primary and Secondary Occupancies**. This dictates EVERYTHING.
-   **Assembly (Group A)**: >50 people? (Requires Voice Evac if >1000 or >300 in some cases).
-   **Educational (Group E)**: Schools. (Strict manual/automatic coverage).
-   **Residential (Group R)**: Hotels/Dormitories vs Apartments. (Sleeping areas require Low Frequency 520Hz sounders).
-   **Business (Group B)**: Offices. (Often manual pull stations + sprinkler monitoring is sufficient).
-   **Storage/Factory (Group S/F)**: Ceiling heights focus.

### 1.2 Physical Geometry & Environmental Analysis
-   **Ceiling Heights**: Crucial for Smoke Detector spacing (stratification) and Strobe candela rating.
    -   *Standard*: 9-10ft.
    -   *High Bay*: >15ft (Requires beam detectors or higher candela).
-   **Room Classifications**:
    -   *Sleepings Rooms*: Must simulate 75dBA (or 15dB > ambient) at the pillow.
    -   *Bathrooms*: Strobe required if public.
    -   *Mechanical/Electrical Rooms*: Heat detectors? Smoke?
-   **Exits & Egress Paths**: Location of "Exit" signs dictates Manual Pull Station placement (<5ft from exit).

---

## Phase 2: Code Research & Application
**Objective**: Establish the "Rule of Law" for this specific project.

### 2.1 The Hierarchy of Authority
1.  **Florida Building Code (FBC) - Building**: The primary scope.
    -   *Chapter 9 (Fire Protection Systems)*: Specifically 907 (Fire Alarm).
2.  **Florida Fire Prevention Code (FFPC)**: Incorporates NFPA 1 at the state level.
3.  **NFPA 72 (National Fire Alarm & Signaling Code)**: The "How-To" manual.
    -   *Ch. 10*: Fundamentals (Power supplies, supervision).
    -   *Ch. 17*: Initiating Devices (Detectors).
    -   *Ch. 18*: Notification Appliances (Audio/Visual).
4.  **NFPA 101 (Life Safety Code)**: The "When-To" manual (Occupancy specifics).
5.  **Local AHJ Amendments**:
    -   *Miami-Dade/Broward*: Often stricter radio responder coverage (Bi-Directional Amplifiers - BDA).

### 2.2 Critical Florida-Specific Checks
-   **Two-Way Radio Enhancement (BDA)**: FBC Section 918. Is signal strength < -95dBm? If so, system required.
-   **Low Frequency (520Hz)**: Mandated for sleeping areas in Hotels/Dormitories/Apartments (since 2014 via NFPA 72).
-   **Survivability**: for Voice Evac, is the circuit integrity Level 2 or 3 (2-hour fire rated cable) required?

---

## Phase 3: Design Implementation Process
**Objective**: Translate requirements into a constructible system.

### 3.1 Initiating Device Layout (Inputs)
-   **Manual Pull Stations**:
    -   Place within 5ft of every Exit discharge.
    -   Ensure travel distance to a pull station is <200ft.
-   **Smoke Detection**:
    -   *Elevator Lobbies*: For elevator recall (Phase I).
    -   *Machine Rooms*: For shunt trip (stop power before sprinkler activation).
    -   *Corridors*: Spacing 30ft on center (radius 21ft). Be mindful of HVAC vents (>3ft away).
-   **Heat Detection**:
    -   Kitchens, Garages, boiler rooms (places where smoke causes false alarms).

### 3.2 Notification Appliance Layout (Outputs)
-   **Audible (Horns/Speakers)**:
    -   Goal: +15dBA above average ambient.
    -   *Public Mode*: Generally >75dBA throughout.
    -   *Private Mode*: Control rooms/Nurse stations.
    -   *Voice Evac*: Required for Assembly > 1000 occupants, High-Rise (>75ft), Elementary Schools.
-   **Visual (Strobes)**:
    -   *Corridors*: <100ft spacing.
    -   *Rooms*: Center wall or ceiling. Candela rating depends on room size (e.g., 20x20 = 15cd, 50x50 = 75cd).
    -   *Sync*: ALL strobes in sight of each other must flash simultaneously to prevent photosensitive epilepsy.

### 3.3 System Architecture (The "Brain")
-   **FACP (Fire Alarm Control Panel)**:
    -   Location: Main entrance or Fire Command Center (for first responders).
    -   Capacity: Point count (Addressable loops). 250 devices per loop?
-   **Power Supplies (NAC Extenders)**:
    -   Voltage Drop: Calculating wire gauge (14AWG vs 12AWG) to ensure devices at the end of the line get >16V (usually).
    -   Battery Calculations: 24 hours standby + 5 minutes alarm (or 15 mins for Voice).

### 3.4 Verification & Permitting
-   **Shop Drawings**: Need Key Plan, Riser Diagram, Battery Calcs, Voltage Drop Calcs.
-   **Signed & Sealed**: By me (Florida PE).
-   **Permit Application**: Submit to local Building Dept & Fire Department.

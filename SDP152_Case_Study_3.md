# SDP152 – Case Study 3
## Pet Records & Booking System (PRBS)

This document contains the use case and class diagrams for the Pet Records & Booking System. The diagrams are based on the eight functional requirements supplied for this case study.

> **Scope note.** The supplied brief also mentions client service requests, equipment tracking, and technician schedules, but it does not define requirements for those capabilities. They are therefore not added to the model below; adding unsupported classes or use cases would change the stated scope. They can be added once their functional requirements are provided.

## Modelling assumptions

- The only human actor in the supplied requirements is an **authorised staff member**. Owners provide information, but staff members enter and maintain it, so owners are not modelled as system users.
- A staff member must successfully log in before using any protected PRBS function.
- A pet has one owner and may have zero or more bookings and alert records.
- A booking must reference exactly one existing pet. A booking cannot be saved with a missing or unknown pet.
- Capacity is checked for the booking's date range. A booking is rejected when accepting it would exceed the daycare facility's maximum capacity.
- A medical or dietary alert is considered active when it contains a current condition, allergy, or dietary restriction. Active alerts are shown on the dashboard.
- Emergency veterinary information belongs to the pet profile and may be updated by staff.
- Owner contact details are stored on the owner profile and captured as a snapshot on a booking so that the contact information used for that booking remains available.

---

# 1. Use case diagram

The diagram expands the broad requirements into the staff interactions needed to operate PRBS. CRUD operations are shown separately so that each responsibility is explicit. The two mandatory booking validations are modelled as `<<include>>` relationships: linking the booking to an existing pet and checking capacity happen before a booking is saved. The dashboard alert is a conditional extension of viewing the dashboard.

```mermaid
flowchart LR
    Staff["Authorised staff member"]

    subgraph PRBS["Pet Records & Booking System (PRBS)"]
        direction TB

        Login(["Log in"])
        Credentials(["Validate username and password"])

        CreatePet(["Create pet profile"])
        ViewPet(["View pet profile"])
        UpdatePet(["Update pet profile"])
        DeletePet(["Delete pet profile"])
        Alerts(["Record or update medical and dietary alerts"])
        EmergencyVet(["Capture emergency veterinary information"])

        Dashboard(["View dashboard"])
        AlertFlag(["Display medical alert flag"])

        CreateBooking(["Create daycare booking"])
        ViewBooking(["View booking"])
        EditBooking(["Edit booking"])
        CancelBooking(["Cancel booking"])
        LinkPet(["Link booking to one existing pet"])
        Capacity(["Check available daycare capacity"])
    end

    Staff --> Login
    Staff --> CreatePet
    Staff --> ViewPet
    Staff --> UpdatePet
    Staff --> DeletePet
    Staff --> Alerts
    Staff --> EmergencyVet
    Staff --> Dashboard
    Staff --> CreateBooking
    Staff --> ViewBooking
    Staff --> EditBooking
    Staff --> CancelBooking

    Login -.->|"<<include>>"| Credentials
    CreateBooking -.->|"<<include>>"| LinkPet
    CreateBooking -.->|"<<include>>"| Capacity
    EditBooking -.->|"<<include when dates change>>"| Capacity
    AlertFlag -.->|"<<extend: active alert exists>>"| Dashboard

    classDef actor fill:#17324d,stroke:#0b1f33,color:#ffffff,stroke-width:2px;
    classDef usecase fill:#e7f2fb,stroke:#2b6f9f,color:#102a43,stroke-width:1.5px;
    classDef validation fill:#fff1cc,stroke:#b7791f,color:#4a2c00,stroke-width:1.5px;
    class Staff actor;
    class Login,CreatePet,ViewPet,UpdatePet,DeletePet,Alerts,EmergencyVet,Dashboard,AlertFlag,CreateBooking,ViewBooking,EditBooking,CancelBooking usecase;
    class Credentials,LinkPet,Capacity validation;
```

### Use case descriptions and requirement traceability

| ID | Use case | Primary actor | Requirement coverage | Result / rule |
|---|---|---|---|---|
| UC-01 | Log in | Authorised staff member | 1 | Credentials are validated before protected functions are available. |
| UC-02 | Create, view, update, and delete pet profile | Authorised staff member | 2 | The profile stores the pet name, breed, age, and owner details. |
| UC-03 | Record or update medical and dietary alerts | Authorised staff member | 3 | Conditions, allergies, and dietary restrictions are stored against the pet. |
| UC-04 | View dashboard and display medical alert flag | Authorised staff member | 4 | An active alert is prominently flagged whenever the dashboard is viewed. |
| UC-05 | Create, view, edit, and cancel daycare booking | Authorised staff member | 5 | The booking stores stay dates, owner contact information, and status. |
| UC-06 | Link booking to one existing pet | PRBS during booking save | 6 | The save is rejected unless the referenced pet already exists. |
| UC-07 | Check available daycare capacity | PRBS during booking save | 7 | The save is rejected when the date range would exceed maximum capacity. |
| UC-08 | Capture emergency veterinary information | Authorised staff member | 8 | Emergency veterinary contact details are stored on the pet profile. |

### Booking validation flow

1. The staff member selects an existing pet and enters the stay dates and owner contact information.
2. PRBS verifies that the pet reference identifies one existing pet.
3. PRBS calculates occupancy for the requested date range and compares it with the facility maximum.
4. Only when both checks pass is the booking saved. If either check fails, the staff member receives a validation error and no booking is created or updated.

### Assignment 1 updates represented here

No Assignment 1 artefact was present in the supplied repository. The following detail has been made explicit in this version so the diagram is traceable to the supplied brief:

- pet profile maintenance is decomposed into create, view, update, and delete interactions;
- alert capture is separated from the dashboard flag that displays the result;
- the emergency veterinary information interaction is included in the pet-profile area;
- booking-to-pet validation and daycare capacity validation are explicit included use cases; and
- authentication is shown as a prerequisite for protected staff functions.

---

# 2. Class diagram

The class diagram separates the core records from the services that enforce the business rules. `Pet`, `Owner`, `MedicalAlert`, `EmergencyVetContact`, and `Booking` represent persistent domain information. The service classes coordinate authentication, profile maintenance, booking validation, capacity checks, and dashboard alert display. Multiplicities show the required booking-to-pet link and the one-owner relationship.

```mermaid
classDiagram
    direction LR

    class StaffAccount {
        <<entity>>
        +UUID staffId
        +String username
        -String passwordHash
        +StaffRole role
        +AccountStatus status
        +DateTime lastLoginAt
        +authenticate(password) Boolean
    }

    class StaffRole {
        <<enumeration>>
        ADMIN
        RECEPTION
        MANAGER
    }

    class AccountStatus {
        <<enumeration>>
        ACTIVE
        LOCKED
        DISABLED
    }

    class Owner {
        <<entity>>
        +UUID ownerId
        +String fullName
        +String phone
        +String email
        +String address
        +updateContactDetails() void
    }

    class Pet {
        <<entity>>
        +UUID petId
        +String name
        +String breed
        +Integer ageYears
        +Boolean hasActiveMedicalAlert()
    }

    class MedicalAlert {
        <<entity>>
        +UUID alertId
        +String medicalConditions
        +String allergies
        +String dietaryRestrictions
        +AlertSeverity severity
        +Boolean active
        +DateTime updatedAt
        +isActive() Boolean
    }

    class AlertSeverity {
        <<enumeration>>
        LOW
        MEDIUM
        HIGH
        CRITICAL
    }

    class EmergencyVetContact {
        <<entity>>
        +UUID contactId
        +String contactName
        +String practiceName
        +String phone
        +String address
    }

    class Booking {
        <<entity>>
        +UUID bookingId
        +Date startDate
        +Date endDate
        +BookingStatus status
        +DateTime createdAt
        +DateTime updatedAt
        +validateDates() Boolean
        +cancel() void
    }

    class OwnerContactSnapshot {
        <<value object>>
        +String fullName
        +String phone
        +String email
    }

    class BookingStatus {
        <<enumeration>>
        CONFIRMED
        CANCELLED
    }

    class DaycareFacility {
        <<entity>>
        +UUID facilityId
        +String name
        +Integer maximumCapacity
        +currentOccupancy(startDate, endDate) Integer
    }

    class AuthenticationService {
        <<service>>
        +login(username, password) StaffAccount
        +logout(staffId) void
    }

    class PetProfileService {
        <<service>>
        +createPet(profileData) Pet
        +getPet(petId) Pet
        +updatePet(petId, profileData) Pet
        +deletePet(petId) void
        +recordAlert(petId, alertData) MedicalAlert
        +captureEmergencyVet(petId, contactData) EmergencyVetContact
    }

    class BookingService {
        <<service>>
        +createBooking(bookingData) Booking
        +getBooking(bookingId) Booking
        +updateBooking(bookingId, bookingData) Booking
        +cancelBooking(bookingId) void
        +validatePetLink(petId) Boolean
        +checkCapacity(bookingData) Boolean
    }

    class CapacityService {
        <<service>>
        +hasAvailability(startDate, endDate) Boolean
        +currentOccupancy(startDate, endDate) Integer
    }

    class Dashboard {
        <<boundary>>
        +displayMedicalAlertFlags() List~MedicalAlert~
    }

    StaffAccount --> StaffRole : has
    StaffAccount --> AccountStatus : has

    Owner "1" --> "0..*" Pet : owns
    Pet "1" *-- "0..*" MedicalAlert : records
    Pet "1" *-- "0..1" EmergencyVetContact : has

    Booking "0..*" --> "1" Pet : for
    Booking "0..*" --> "1" Owner : contact owner
    Booking "1" *-- "1" OwnerContactSnapshot : stores
    Booking "0..*" --> "1" DaycareFacility : booked at
    Booking --> BookingStatus : has

    MedicalAlert --> AlertSeverity : has

    AuthenticationService ..> StaffAccount : authenticates
    PetProfileService ..> Pet : maintains
    PetProfileService ..> MedicalAlert : records and updates
    PetProfileService ..> EmergencyVetContact : captures
    BookingService ..> Booking : manages
    BookingService ..> Pet : requires existing pet
    BookingService ..> Owner : reads contact details
    BookingService ..> CapacityService : requests check
    CapacityService ..> DaycareFacility : reads maximum capacity
    CapacityService ..> Booking : counts active bookings
    Dashboard ..> Pet : reads profiles
    Dashboard ..> MedicalAlert : displays active flags
```

### Class responsibilities and constraints

| Class / group | Responsibility |
|---|---|
| `StaffAccount` and enumerations | Stores authorised staff credentials and account state. The password is represented as a hash rather than plaintext. |
| `Owner` | Stores owner identity and contact details used by pet profiles and bookings. |
| `Pet` | Stores the required pet profile data and acts as the parent for medical alerts and emergency veterinary information. |
| `MedicalAlert` | Stores medical conditions, allergies, and dietary restrictions, including severity and whether the alert is active. |
| `EmergencyVetContact` | Stores the emergency veterinary contact captured for a pet. |
| `Booking` | Stores stay dates, status, the required pet reference, owner reference, and a contact snapshot. |
| `DaycareFacility` and `CapacityService` | Represent maximum capacity and the occupancy check used before a booking is saved. |
| `AuthenticationService` | Enforces the login prerequisite. |
| `PetProfileService` | Performs pet CRUD operations and captures alert and emergency veterinary data. |
| `BookingService` | Performs booking CRUD/cancellation and coordinates pet-link and capacity validation. |
| `Dashboard` | Reads active alerts and presents the medical alert flag to staff. |

### Important multiplicities

- `Booking "0..*" --> "1" Pet`: every booking has exactly one existing pet; a pet may have many bookings over time.
- `Owner "1" --> "0..*" Pet`: every pet has one owner; an owner may have multiple pets.
- `Pet "1" *-- "0..*" MedicalAlert`: a pet may have no alerts or several alert records; only active records are shown on the dashboard.
- `Booking "1" *-- "1" OwnerContactSnapshot`: every booking retains the owner contact information used for that booking.
- `Booking "0..*" --> "1" DaycareFacility`: capacity is evaluated against the facility where the booking is made.

## Diagram source files

The standalone PlantUML source files are included alongside this document for editing or rendering:

- [`docs/prbs-use-case.puml`](docs/prbs-use-case.puml)
- [`docs/prbs-class-diagram.puml`](docs/prbs-class-diagram.puml)

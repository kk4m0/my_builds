# PetPause Daycare – PRBS
## Overview of the Chosen Agile Method: Iterative and Incremental Development (IID)

The Pet Records & Booking System (PRBS) will be built using **iterative and incremental development (IID)**, the agile approach in which a system is grown through a series of short, repeated development cycles rather than delivered in one large hand-over at the end of the project.

In my own words, IID combines two complementary ideas. The *incremental* part means the system is sliced into small pieces of working functionality, and each slice is built, tested and released so the product grows feature by feature. The *iterative* part means each cycle also revisits and refines what already exists: earlier code, designs and requirements are improved in light of feedback, defects and new understanding. Larman and Basili describe the process as starting "with a simple implementation of a subset of the software requirements" and iteratively enhancing "the evolving sequence of versions until the full system is implemented," with design modifications made at each iteration alongside new capability (Larman & Basili, *Iterative and Incremental Development: A Brief History*, IEEE Computer, 2003).

For PRBS this fits the business risk directly. The trigger for the project — a smudged medical note that endangered an animal — means safety-critical features cannot wait. High-priority requirements are therefore scheduled first: staff authentication and failed-attempt logging (FR1–FR2), pet profiles with mandatory emergency vet details (FR3–FR5), then bookings linked to exactly one pet (FR6–FR8), the capacity check (FR9), dashboard medical alerts (FR10) and daily status tracking (FR11). Medium-priority reporting (FR12) follows in a later increment.

Each iteration ends with a demonstrable, tested build that PetPause staff can review, so misunderstandings about capacity rules or alert visibility surface in weeks rather than months. Feedback then reshapes the backlog for the next cycle, allowing the team to adapt while continuously delivering value and reducing risk.

*(Word count of overview body: ~300)*

**Reference**
Larman, C. & Basili, V. R. (2003) 'Iterative and Incremental Development: A Brief History', *IEEE Computer*, 36(6), pp. 47–56. Available at: https://www.craiglarman.com/wiki/downloads/misc/history-of-iterative-larman-and-basili-ieee-computer.pdf

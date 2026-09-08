# PetPause Daycare – PRBS
## Overview of the Chosen Agile Method: Iterative and Incremental Development (IID)

The Pet Records & Booking System (PRBS) will be built using **iterative and incremental development (IID)**, the agile approach in which a system is grown through a series of short, repeated development cycles rather than delivered in one large hand-over at the end of the project.

In my own words, IID combines two complementary ideas. The *incremental* part means the system is sliced into small pieces of working functionality, and each slice is built, tested and released so the product grows feature by feature. The *iterative* part means each cycle also revisits and refines what already exists: earlier code, designs and requirements are improved in light of feedback, defects and new understanding. Larman and Basili (2003) describe the process as starting "with a simple implementation of a subset of the software requirements" and iteratively enhancing "the evolving sequence of versions until the full system is implemented," with design modifications made at each iteration alongside new capability.

For PRBS this fits the business risk directly. The trigger for the project — a smudged medical note that endangered an animal — means safety-critical features cannot wait. High-priority requirements are therefore scheduled first: staff authentication and failed-attempt logging (FR1–FR2), pet profiles with mandatory emergency vet details (FR3–FR5), then bookings linked to exactly one pet (FR6–FR8), the capacity check (FR9), dashboard medical alerts (FR10) and daily status tracking (FR11). Medium-priority reporting (FR12) follows in a later increment.

Each iteration ends with a demonstrable, tested build that PetPause staff can review, so misunderstandings about capacity rules or alert visibility surface in weeks rather than months. Feedback then reshapes the backlog for the next cycle, allowing the team to adapt while continuously delivering value and reducing risk.

*(Word count of overview body: ~300)*

## References

**Primary source cited in the overview**

- Larman, C. and Basili, V.R. (2003) 'Iterative and incremental development: a brief history', *Computer*, 36(6), pp. 47–56. Available at: https://doi.org/10.1109/MC.2003.1204375 (Accessed: 08 September 2026).

**Additional credible sources**

- Agile Alliance (no date a) *Incremental development*. Available at: https://agilealliance.org/glossary/incremental-development/ (Accessed: 08 September 2026).
- Agile Alliance (no date b) *Iterative development*. Available at: https://agilealliance.org/glossary/iterative-development/ (Accessed: 08 September 2026).
- Beck, K., Beedle, M., van Bennekum, A., Cockburn, A., Cunningham, W., Fowler, M., Grenning, J., Highsmith, J., Hunt, A., Jeffries, R., Kern, J., Marick, B., Martin, R.C., Mellor, S., Schwaber, K., Sutherland, J. and Thomas, D. (2001) *Manifesto for agile software development*. Available at: https://agilemanifesto.org/ (Accessed: 08 September 2026).
- Boehm, B.W. (1988) 'A spiral model of software development and enhancement', *Computer*, 21(5), pp. 61–72. Available at: https://doi.org/10.1109/2.59 (Accessed: 08 September 2026).
- Schwaber, K. and Sutherland, J. (2020) *The Scrum Guide*. Available at: https://scrumguides.org/scrum-guide.html (Accessed: 08 September 2026).

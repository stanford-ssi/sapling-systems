# Link Budgets

## Rough Plan of Attack

Run antenna simulations in `4nec2`, and then use pylink-satcom
to simulate the RF links, and then use Python to simulate the
data encoding and generate plots of SNR vs Error rate. In
addition, use Python to generate graphs of link margin over
the course of a couple of ground pass profiles, and generate
statistics of data per ground pass, average number of ground
passes per day, and data throughput.

<https://arxiv.org/pdf/1905.11252.pdf>

## Current Needs

- Figure out RX and TX efficiencies and es/n0 (not SNR) for both LoRa
and frequency hopping.

- Read more about radios and determine components with greater accuracy
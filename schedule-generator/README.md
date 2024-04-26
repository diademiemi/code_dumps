# Schedule Generator (Made with the help of ChatGPT-4)
This is a simple script that generates a schedule for people based on availability per day. I don't expect this to be useful for many, but I figured I'd upload it here in case someone finds it useful.

The usecase for this was to generate an OpsGenie schedule for a team based on their availability per day. The script takes in a JSON object like the following:
```json
{"mon": ["P1", "P2", "P3", "P4", "P5", "P6", "P7"],"tue": ["P1", "P2", "P3", "P4", "P5", "P6", "P7"],"wed": ["P1", "P2", "P3", "P5", "P6", "P7"],"thu": ["P1", "P2", "P3", "P4", "P5", "P6", "P7"],"fri": ["P2", "P3", "P4", "P5", "P6", "P7"]}

```

Where the keys are the days of the week and the values are the people available on that day. The script then generates a schedule for each day based on the availability of the people.

Example output:
```c
Amount of people: 7
Week 1: P2, P1, P5, P7, P4
Week 2: P3, P7, P5, P6, P4
Week 3: P1, P6, P5, P2, P4
Week 4: P1, P3, P7, P2, P4
Week 5: P2, P6, P7, P3, P5
Week 6: P1, P6, P7, P3, P4
Week 7: P2, P6, P1, P5, P3
```

The script is far from perfect, but it works for our usecase. Feel free to modify it to suit your needs.

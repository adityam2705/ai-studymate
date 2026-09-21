"""Clearly labelled built-in content for offline demonstrations."""

DEMO_SUMMARY = """# Operating Systems: Process Management

## Overview
An operating system manages computer hardware and provides services to programs. A **process** is a program that is currently being executed.

## Key Concepts
- **Process Control Block (PCB):** Stores process information such as its state, program counter, registers, and scheduling details.
- **Process states:** A process can be New, Ready, Running, Waiting, or Terminated.
- **CPU scheduling:** The operating system selects a process from the ready queue to use the CPU.
- **Context switch:** The operating system saves one process's state and restores another process's state. This creates overhead.

## Important Definitions
- **Ready queue:** Processes prepared to run when the CPU becomes available.
- **Waiting state:** A process is waiting for an event such as input/output to finish.
- **Scheduler:** The OS component that chooses the next process for execution.

## Remember
Processes improve multitasking, but frequent context switches can reduce performance because the CPU spends time switching instead of executing useful work.
"""

DEMO_QUIZ = [
    {
        "question": "What is a process in an operating system?",
        "options": {
            "A": "A program that is currently executing",
            "B": "A physical CPU component",
            "C": "A type of input device",
            "D": "A file stored on a disk",
        },
        "correct_answer": "A",
        "explanation": "A process is an active instance of a program being executed.",
    },
    {
        "question": "Which structure stores information about a process?",
        "options": {
            "A": "Ready Queue",
            "B": "Process Control Block",
            "C": "Context Switch",
            "D": "CPU Register",
        },
        "correct_answer": "B",
        "explanation": "The Process Control Block, or PCB, stores the process state and other details.",
    },
    {
        "question": "What happens during a context switch?",
        "options": {
            "A": "The computer shuts down",
            "B": "A process is deleted",
            "C": "The OS saves one process state and restores another",
            "D": "A new hard disk is installed",
        },
        "correct_answer": "C",
        "explanation": "A context switch changes the CPU from one process to another by saving and restoring states.",
    },
    {
        "question": "A process waiting for input/output is in which state?",
        "options": {
            "A": "Running",
            "B": "Ready",
            "C": "Waiting",
            "D": "New",
        },
        "correct_answer": "C",
        "explanation": "A process enters the Waiting state until the required event, such as I/O completion, occurs.",
    },
    {
        "question": "What is the main role of CPU scheduling?",
        "options": {
            "A": "To select a ready process for CPU execution",
            "B": "To print documents",
            "C": "To remove all processes",
            "D": "To increase disk size",
        },
        "correct_answer": "A",
        "explanation": "CPU scheduling chooses which ready process receives the CPU next.",
    },
]

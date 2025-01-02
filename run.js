const { spawn } = require('child_process');

function createChildProcess(command, args, cwd) {
    const child = spawn(command, args, { cwd, shell: true });

    child.stdout.on('data', (data) => {
        console.log(`[${cwd} stdout]: ${data}`);
    });

    child.stderr.on('data', (data) => {
        console.error(`[${cwd} stderr]: ${data}`);
    });

    child.on('close', (code) => {
        console.log(`[${cwd}] exited with code ${code}`);
    });

    return child;
}

// Create child processes
const processes = [
    createChildProcess('bash', ['-c', 'gcc sort.c -o sort && while true; do ./sort; done'], 'c'),
    createChildProcess('bash', ['-c', 'javac sort.java && while true; do java sort; done'], 'java'),
    createChildProcess('bash', ['-c', 'while true; do cargo run; done'], 'rust'),
    createChildProcess('bash', ['-c', 'while true; do python sort.py; done'], 'python'),
];

function terminateProcesses() {
    processes.forEach((child) => {
        if (child && !child.killed) {
            child.kill('SIGTERM');
        }
    });
    process.exit();
}

process.on('SIGINT', terminateProcesses);
process.on('SIGTERM', terminateProcesses);

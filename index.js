const { spawn } = require('child_process');
const XLSX = require('xlsx');
const fs = require("fs");

function createExcelWithJSON(data, fileName) {
    const workbook = XLSX.utils.book_new();

    for (const [sheetName, sheetData] of Object.entries(data)) {
        const worksheet = XLSX.utils.json_to_sheet(sheetData);
        XLSX.utils.book_append_sheet(workbook, worksheet, sheetName);
    }

    XLSX.writeFile(workbook, fileName);
}

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

const processes = [
    createChildProcess('bash', ['-c', 'cd c && gcc sort.c -o sort && while true; do ./sort; done'], 'c'),
    createChildProcess('bash', ['-c', 'cd java && javac sort.java && while true; do java sort; done'], 'java'),
    createChildProcess('bash', ['-c', 'cd rust && while true; do cargo run; done'], 'rust'),
    createChildProcess('bash', ['-c', 'cd python && while true; do python sort.py; done'], 'python'),
];

function readAndSplitData(filePath) {
    const data = fs.readFileSync(filePath, 'utf8');
    return data.split("\n\n");
}

function terminateProcesses() {
    processes.forEach((child) => {
        if (child && !child.killed) {
            child.kill('SIGTERM');
        }
    });
    process.exit();
}

function handleOnClose() {
    const filePaths = {
        "C": './c/log.txt',
        "Java": './java/log.txt',
        "Python": './python/log.txt',
        "Rust": './rust/log.txt'
    };

    const dataArrays = {};
    for (const [language, path] of Object.entries(filePaths)) {
        dataArrays[language] = readAndSplitData(path);
    }

    const trials = Math.min(...Object.values(dataArrays).map(arr => arr.length));

    const sheetsData = {
        "Execution Time in miliseconds": [],
        "CPU Usage percentage": [],
        "Memory Usage in kilobytes": []
    };

    for (let i = 0; i < trials - 1; i++) {
        const memoryRow = { "Iteration": i + 1 };
        const executionRow = { "Iteration": i + 1 };
        const cpuRow = { "Iteration": i + 1 };
    
        for (const [language, array] of Object.entries(dataArrays)) {
            const lines = array[i] ? array[i].split("\n") : [];
            const memoryUsage = parseFloat(lines[2] ? lines[2].split(" ").slice(-2, -1)[0] : "0");
            const executionTime = parseFloat(lines[1] ? lines[1].split(" ").slice(-1)[0].replace("ms", "") : "0");
            const cpuUsage = parseFloat((lines[3] ? lines[3].split(" ").slice(-1)[0] : "0").replace("%", ""));
    
            memoryRow[language] = memoryUsage;
            executionRow[language] = executionTime;
            cpuRow[language] = cpuUsage;
        }
    
        sheetsData["Memory Usage in kilobytes"].push(memoryRow);
        sheetsData["Execution Time in miliseconds"].push(executionRow);
        sheetsData["CPU Usage percentage"].push(cpuRow);
    }    
    

    createExcelWithJSON(sheetsData, "Output_log.xlsx");
    terminateProcesses();
}

process.on('SIGINT', handleOnClose);
process.on('SIGTERM', handleOnClose);

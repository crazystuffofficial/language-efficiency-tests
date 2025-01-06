use std::fs::OpenOptions;
use std::io::{BufRead, BufReader, Write};
use std::time::Instant;

fn read_cpu_stats() -> Vec<u64> {
    let file = std::fs::File::open("/proc/stat").expect("Unable to open /proc/stat");
    let reader = BufReader::new(file);
    let first_line = reader.lines().next().expect("Failed to read first line").expect("Empty /proc/stat");
    if first_line.starts_with("cpu ") {
        first_line
            .split_whitespace()
            .skip(1)
            .map(|v| v.parse::<u64>().expect("Invalid CPU stat"))
            .collect()
    } else {
        panic!("Unexpected format in /proc/stat");
    }
}

fn calculate_total(stats: &[u64]) -> u64 {
    stats.iter().copied().sum()
}

fn main() {
    let size = 1_000_000;
    let mut arr: Vec<u32> = (0..size as u32).rev().collect();

    // Read initial CPU stats
    let cpu_stats_before = read_cpu_stats();
    let total_before = calculate_total(&cpu_stats_before);
    let idle_before = cpu_stats_before[3];

    // Measure execution time
    let start_time = Instant::now();
    arr.sort_by(|a, b| b.cmp(a));
    let duration = start_time.elapsed();

    // Read final CPU stats
    let cpu_stats_after = read_cpu_stats();
    let total_after = calculate_total(&cpu_stats_after);
    let idle_after = cpu_stats_after[3];

    // Calculate CPU usage percentage
    let idle_diff = idle_after - idle_before;
    let total_diff = total_after - total_before;
    let cpu_usage = 100.0 * (1.0 - (idle_diff as f64 / total_diff as f64));

    // Memory usage (Linux-specific)
    #[cfg(target_os = "linux")]
    let memory_usage = {
        let statm_path = "/proc/self/statm";
        let statm_content = std::fs::read_to_string(statm_path).expect("Unable to read /proc/self/statm");
        let resident_pages: u64 = statm_content
            .split_whitespace()
            .nth(1)
            .expect("Invalid statm format")
            .parse()
            .expect("Invalid resident size");
        resident_pages * 4096
    };

    #[cfg(not(target_os = "linux"))]
    let memory_usage = 0;

    // Log results
    let mut file = OpenOptions::new()
        .append(true)
        .create(true)
        .open("log.txt")
        .unwrap();
    writeln!(
        file,
        "Rust:\nExecution time: {:.2?}\nMemory usage: {} KB\nCPU usage: {:.2}%\n",
        duration,
        memory_usage / 1024,
        cpu_usage
    )
    .unwrap();
}

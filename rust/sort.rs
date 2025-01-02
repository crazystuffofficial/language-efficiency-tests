use std::fs::OpenOptions;
use std::io::Write;
use std::time::Instant;
use sysinfo::{CpuExt, System, SystemExt};
#[cfg(target_os = "linux")]
use procfs;
fn main() {
    let size = 1_000_000;
    let mut arr: Vec<u32> = (0..size as u32).rev().collect();
    let mut system = System::new_all();
    system.refresh_all();
    let start_cpu_usage = system.cpus().iter().map(|cpu| cpu.cpu_usage()).sum::<f32>() / system.cpus().len() as f32;
    let start_time = Instant::now();
    arr.sort_by(|a, b| b.cmp(a));
    let duration = start_time.elapsed();
    system.refresh_all();
    let end_cpu_usage = system.cpus().iter().map(|cpu| cpu.cpu_usage()).sum::<f32>() / system.cpus().len() as f32;
    let cpu_usage_change = end_cpu_usage - start_cpu_usage;
    #[cfg(target_os = "linux")]
    let memory_usage = procfs::process::Process::myself()
        .and_then(|p| p.statm())
        .map(|statm| statm.resident * 4096)
        .unwrap_or(0);
    #[cfg(not(target_os = "linux"))]
    let memory_usage = 0;
    let mut file = OpenOptions::new()
        .append(true)
        .create(true)
        .open("log.txt")
        .unwrap();
    writeln!(
        file,
        "Rust:\nExecution time: {:.2?}\nMemory usage: {} KB\nCPU usage change: {:.2}%\n",
        duration,
        memory_usage / 1024,
        cpu_usage_change
    )
    .unwrap();
}
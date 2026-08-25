import argparse
import xml.etree.ElementTree as ET


def generate_report(xml_file, output_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    report_lines = ["# Nmap Scan Report", ""]

    host_count = 0
    open_port_count = 0

    for host in root.findall("host"):
        host_count += 1

        address = host.find("address[@addrtype='ipv4']")
        host_ip = address.get("addr") if address is not None else "unknown"

        status = host.find("status")
        host_status = status.get("state") if status is not None else "unknown"

        report_lines.append(f"## Host: {host_ip}")
        report_lines.append("")
        report_lines.append(f"**Status:** {host_status}")
        report_lines.append("")
        report_lines.append("| Port | Protocol | State | Service | Product / Version |")
        report_lines.append("|---|---|---|---|---|")

        ports = host.find("ports")

        if ports is not None:
            for port in ports.findall("port"):
                port_id = port.get("portid")
                protocol = port.get("protocol")

                state = port.find("state")
                state_name = state.get("state") if state is not None else "unknown"

                if state_name != "open":
                    continue

                open_port_count += 1

                service = port.find("service")

                service_name = service.get("name", "unknown") if service is not None else "unknown"
                product = service.get("product", "") if service is not None else ""
                version = service.get("version", "") if service is not None else ""
                product_version = f"{product} {version}".strip()

                report_lines.append(
                    f"| {port_id} | {protocol.upper()} | {state_name} | {service_name} | {product_version or '-'} |"
                )

        report_lines.append("")

    report_lines.append("## Summary")
    report_lines.append("")
    report_lines.append(f"- Hosts processed: {host_count}")
    report_lines.append(f"- Open ports discovered: {open_port_count}")

    with open(output_file, "w", encoding="utf-8") as report_file:
        report_file.write("\n".join(report_lines))

    print(f"Report generated: {output_file}")
    print(f"Hosts processed: {host_count}")
    print(f"Open ports discovered: {open_port_count}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert Nmap XML output into a Markdown report."
    )

    parser.add_argument(
        "xml_file",
        help="Path to the Nmap XML file"
    )

    parser.add_argument(
        "-o",
        "--output",
        default="report.md",
        help="Output Markdown file (default: report.md)"
    )

    args = parser.parse_args()
    generate_report(args.xml_file, args.output)


if __name__ == "__main__":
    main()

<#
PowerShell script that exports Norton Security logs and converts the logs to separate csv files for Splunk. Here's a quick description:

First, it runs a commmand that exports the logs from Norton.
Next, it regex matches relevant sections from the logs and redirects the matches to separate text files. The relevant sections I chose to keep from the Logs are:
To start the csv conversion process, it removes the title and headers and then exports as a new text file.
Finally, it adds new headers with import-csv and uses export-csv to convert the file to a csv with separated columns.
The end result is titled csv security logs that can be loaded to Splunk with a universal forwarder. The csv files are nice because Splunk reads the headers and makes them into fields for efficient analyzing.
#>


#EXPORT LOGS FROM NORTON SECURITY APPLICATION
C:\"Program Files"\"Norton Security"\Engine\22.14.0.54\mcui32.exe /export c:\Users\*****\Desktop\NortonLogs\logs.txt

Start-sleep 20

#NAME OF LOGS: logs.txt
$recent_history = Get-Content logs.txt -Raw

#RECENT-HISTORY LOGS
$recent_history -match '(?s)(Category: Recent History.*?)(?:(?:\r*\n){3})'
$matches[1] > recent_history.txt
Get-Content recent_history.txt | Select-Object -Skip 2 | Out-File recent_history1.txt
import-csv recent_history1.txt -Header "Date & Time", "Risk", "Activity", "Status" | Export-Csv recent_history.csv

#SCAN-RESULTS LOGS
$recent_history -match '(?s)(Category: Scan Results.*?)(?:(?:\r*\n){3})'
$matches[1] > scan_results.txt
Get-Content scan_results.txt | Select-Object -Skip 2 | Out-File scan_results1.txt
import-csv scan_results1.txt -Header 'Date & Time', 'Risk', 'Activity', 'Status', 'Scan Time (d:h:m:s)', 'Total items scanned', 'Files & Directories', 'Registry Entries', 'Processes & Startup Items', 'Network & Browser Items', 'Other', 'Trusted Files', 'Skipped Files', 'Total Security Risks Detected', 'Total Security Risks Resolved', 'Total Security Risks Requiring Attention', 'Recommended Action' | Export-Csv scan_results.csv

#RESOLVED_RISKS LOGS
$recent_history -match '(?s)(Category: Resolved Security Risks.*?)(?:(?:\r*\n){3})'
$matches[1] > resolved_risks.txt
Get-Content resolved_risks.txt | Select-Object -Skip 2 | Out-File resolved_risks1.txt
import-csv resolved_risks1.txt -Header 'Date & Time','Risk','Activity','Status','Recommended Action','Activity - Details' | Export-Csv resolved_risks.csv

#FIREWALL_CONNECTIONS LOGS
$recent_history -match '(?s)(Category: Firewall - Network and Connections.*?)(?:(?:\r*\n){3})'
$matches[1] > firewall_connections.txt
Get-Content firewall_connections.txt | Select-Object -Skip 2 | Out-File firewall_connections1.txt
import-csv firewall_connections1.txt -Header 'Date & Time','Risk','Activity','Status','Recommended Action','Gateway Physical Address','Category','Subnet Identifier' | Export-Csv firewall_connections.csv

#FIREWALL_ACTIVITIES LOGS
$recent_history -match '(?s)(Category: Firewall - Activities.*?)(?:(?:\r*\n){3})'
$matches[1] > firewall_activities.txt
Get-Content firewall_activities.txt | Select-Object -Skip 2 | Out-File firewall_activities1.txt
import-csv firewall_activities1.txt -Header 'Date & Time','Risk','Activity','Status','Recommended Action','Category' | Export-Csv firewall_activities.csv

#INTRUSION_PREVENTION LOGS
$recent_history -match '(?s)(Category: Intrusion Prevention.*?)(?:(?:\r*\n){3})'
$matches[1] > intrusion_prevention.txt
Get-Content intrusion_prevention.txt | Select-Object -Skip 2 | Out-File intrusion_prevention1.txt
import-csv intrusion_prevention1.txt -Header 'Date & Time','Risk','Activity','Status','Recommended Action','Category','Default Action','Action Taken','IPS Alert Name','Attacking Computer','Attacker URL','Destination Address','Source Address','Traffic Description' | Export-Csv intrusion_prevention.csv

#DOWNLOAD_INSIGHT LOGS
$recent_history -match '(?s)(Category: Download Insight.*?)(?:(?:\r*\n){3})'
$matches[1] > download_insight.txt
Get-Content download_insight.txt | Select-Object -Skip 2 | Out-File download_insight1.txt
import-csv download_insight1.txt -Header 'Date & Time','Risk','Activity','Status','Activity - Details' | Export-Csv download_insight.csv

#ANTI-SPAM LOGS
$recent_history -match '(?s)(Category: AntiSpam.*?)(?:(?:\r*\n){3})'
$matches[1] > antispam.txt
Get-Content antispam.txt | Select-Object -Skip 2 | Out-File antispam1.txt
import-csv antispam1.txt -Header 'Date & Time','Risk','Activity','Status','Recommended Action' | Export-Csv antispam.csv

#IDENTITY LOGS
$recent_history -match '(?s)(Category: Identity.*?)(?:(?:\r*\n){3})'
$matches[1] > identity.txt
Get-Content identity.txt | Select-Object -Skip 2 | Out-File identity1.txt
import-csv antispam1.txt -Header 'Date & Time','Risk','Activity','Status','Recommended Action' | Export-Csv antispam.csv

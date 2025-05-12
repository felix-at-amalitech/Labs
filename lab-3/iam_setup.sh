#!/bin/bash

user_file="$1"
group_file="$2"
timestamp=$(date '+%Y-%m-%d_%H-%M-%S')
log_file="${timestamp}_iam_logs.txt"

# Initialize log file with timestamp
echo "Script started at $(date)" > "$log_file"

# Step 1: Read groups and ensure they exist
echo "Checking and creating groups... " | tee -a "$log_file"
valid_groups=()

while read -r line; do
  line=$(echo "$line" | xargs)
  [[ -z "$line" || "$line" =~ ^# ]] && continue
  valid_groups+=("$line")
  if ! getent group "$line" > /dev/null; then
    echo "Creating group: $line" | tee -a "$log_file"
    sudo groupadd "$line" 2>&1 | tee -a "$log_file"
  else
    echo "Group '$line' already exists." | tee -a "$log_file"
  fi
done < "$group_file"

# Step 2 & 3: Read users, check and create each user in their group
echo -e "\n Processing users from $user_file..." | tee -a "$log_file"
tail -n +2 "$user_file" | while IFS=',' read -r username fullname group email password; do
  username=$(echo "$username" | xargs)
  fullname=$(echo "$fullname" | xargs)
  fullname=${fullname// /_}
  email=$(echo "$email" | xargs)
  password=$(echo "$password" | xargs)
  group=$(echo "$group" | xargs)

  # Ensure the group is one of the valid ones
  if [[ ! " ${valid_groups[*]} " =~ " $group " ]]; then
    echo "Skipping user '$username': group '$group' is not in valid group list." | tee -a "$log_file"
    continue
  fi

  # Create the user if not already present
  if ! id "$username" > /dev/null 2>&1; then
    echo "Creating user: $username ($fullname) in group $group" | tee -a "$log_file"
    sudo useradd -m -c "$fullname" -g "$group" "$username" 2>&1 | tee -a "$log_file"
    sudo chmod 700 "/home/$username" 2>&1 | tee -a "$log_file"


    # Set default password
    echo "$username:$password" | sudo chpasswd 2>&1 | tee -a "$log_file"

    # Force password change on first login
    sudo chage -d 0 "$username" 2>&1 | tee -a "$log_file"

    # Send welcome email
    mail_subject="Welcome to the system, $fullname"
    mail_body="Hi $fullname,\n\nYour linux account with '$username' has been created.\nYour temporary password is:$password \nPlease change it on first login.\n\nThanks,\nAdmin Team"

    if echo -e "$mail_body" | mail -s "$mail_subject" "$email" 2>>"$log_file"; then
      echo "Welcome email sent to $email" | tee -a "$log_file"
    else
      echo "Failed to send email to $email" | tee -a "$log_file"
    fi

  else
    echo "User '$username' already exists." | tee -a "$log_file"
  fi
done

echo "Script finished at $(date)" | tee -a "$log_file"

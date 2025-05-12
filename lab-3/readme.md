# How to use iam_setup.sh

1. create a file "user_file" that contains comma separated user information with the columns.  

2. add users following csv template below

    ```sh
    username,fullname,group,email,password
    jdoe,John Doe,engineering,felix.frimpong@amalitechtraining.org,TempPass123!
    ```

3. create a file "group_file"

4. add groups to the file, one group per line

    ```sh
    group1
    group2
    group3
    ```

5. To run the script, execute

```sh
  iam_setup.sh user_file group_file
```

## Logging

Logs are creted everytime the script is run with datetime_scriptname.txt

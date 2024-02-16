def towerofhanoi(disk_number, source, destination, helper):
    if disk_number == 1:
        print(f"Move disk 1 from source {source} to destination {destination}")
        return
    towerofhanoi(disk_number - 1, source, helper, destination)
    print(f"Move disk {disk_number} from source {source} to destination {destination}")
    towerofhanoi(disk_number - 1, helper, destination, source)

    
disk_number = int(input("Enter the number of disks: "))
towerofhanoi(disk_number, "A", "B", "C")
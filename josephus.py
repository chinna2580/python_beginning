def josephus(people, step=2):
  if step<=1:
    print("Enter step value, greater than 1")
  else:
    step -= 1 # translated to zero-based indexing
    kill = step # kill will hold the index of current person to die
    while(len(people) > 1):
      print(people.pop(kill)) # pop method removes the element from the list
      kill = (kill + step) % len(people) 
    print(people[0], "is safe")
   
num = int(input("Enter the number of soldiers:  "))
soldiers = [i for i in range(1, num+1)] # generates a list of 1..num
josephus(soldiers)
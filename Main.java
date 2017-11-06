public class Main{
  public static void main(String[] args){
    Clock MyClock = new Clock(0, 0, 8, true);
    MyClock.tellTime();
    MyClock.advanceTime(111);
    MyClock.tellTime();
  } 
}



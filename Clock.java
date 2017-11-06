public class Clock{

  // Initialization of Variables

  private int curHour;  

  private int curMin;

  private int alarm;

  private boolean clockFormat; // True for 24-hour, False for 12-hour format

  // Constructor

  public Clock(int startcurHour, int startcurMin, int startalarm,  boolean startclockFormat){
    curHour = startcurHour;
    curMin = startcurMin;
    alarm = startalarm;
    clockFormat = startclockFormat;
  }

  // Getters

  public int getalarm(){
    return alarm;
  }

  public int getcurHour(){
    return curHour;
  }
  
  public int getcurMin(){
    return curMin;
  }

  public boolean getclockFormat(){
    return clockFormat;
  }

  // Setters
  public void setalarm(int newValue){
    alarm = newValue;
  }

  public void setcurHour(int newValue){
    curHour = newValue;
  }
  
  public void setcurMin(int newValue){
    curMin = newValue;
  }

  public void setclockFormat(boolean newValue){ 
    clockFormat = newValue;
  }
  
  // Methods
  public void advanceTime(int shiftTime)
  {
    int totalmin = (this.curHour * 60) + this.curMin + shiftTime;
    
    if(this.clockFormat == true){
      this.curHour = totalmin / 60;
      if(this.curHour >= 24) this.curHour = this.curHour - 24;

      this.curMin = totalmin % 60;
    }
        
    if(this.clockFormat == false){
      this.curHour = totalmin / 60;
      if(this.curHour >= 12) this.curHour = this.curHour - 12;

      this.curMin = totalmin % 60;
    } 
    return;
  }

  public void tellTime()
  {
    System.out.println(("The current hour is ") + this.curHour + ( ":" ) + this.curMin);
    return;
  }

}
  

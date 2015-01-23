// This is what we are going to send to the pc when the user
// has made his move, the pc will then do what he has to do
#define MOVE_MADE '1'

#define LED 13        // led pin used for debug 
                      // and to tell user wrong move

// definition of macros for pins associated wih motor 1
// motor 1 controlls the movement in y direction
#define DIR1 4
#define STP1 5
#define EN1 6

//definition of macros for pins associated with motor 2
#define DIR2 7
#define STP2 8
#define EN2 9

// macro for the magnet pin
#define MAGNET 10

// macro for button pin
#define MOVE_BUTTON 2

// End definition macros=========================================================================================

// Definition of variables========================================================================================
const float prec_m = 0.02;          // doing 1 step will move the belt by prec_m cm
const float size_square = 4.5;      // size of the squares in cm
const unsigned int steps_deviation = (int) (size_square/2)/prec_m; // steps needed to move piece from center to border of square

int pos_coord[2] = {1, 1};          // current position of the motor, motor should be placed at {1,1} before starting the arduino
int move_begin[2] = {1, 1};         // coordinates of the pice that has to be moved
int move_end[2] = {1, 1};           // coordinated of the position tho where the piece has been moved
int jail_coord[2] = {9, 5};   // Jail : fallen pieces get moved to this position

/* control variable, this will determine if we have an invalid move, 
 a piece will go to jail or the move consits in a simple motion of the piece
 
 ctrl = '0' => normal move
 ctrl = '1' => piece will go to jail
 ctrl = '2' => invalid move
*/
char ctrl;

boolean moveRecieved = false;       // flag to see if we got a move or not so that we don't make the move twice

String data;                        //contains the information sent by the PC

// End Variable definitions =====================================================================================

void setup(){
  Serial.begin(9600);
  
  // Definition of the pinMode for motor 1
  pinMode(STP1,OUTPUT);
  pinMode(DIR1,OUTPUT);
  pinMode(EN1,OUTPUT);
  
  // Defintion of the pinMode for motor 2
  pinMode(STP2,OUTPUT);
  pinMode(DIR2,OUTPUT);
  pinMode(EN2,OUTPUT);
  
  // Config for Led
  pinMode(LED,OUTPUT);
  // Config for Magnet
  pinMode(MAGNET,OUTPUT);
  // Config for buttin
  pinMode(MOVE_BUTTON,INPUT);
  
  // Disable the motors just to be sure
  disableMotors();
  digitalWrite(MAGNET,LOW);
  //Serial.println("SETUP DONE");
  delay(100);
}

void loop() {
  digitalWrite(MAGNET,LOW);
  delay(100);
  
  if (!moveRecieved && digitalRead(MOVE_BUTTON) == HIGH) {
    // The user pushed the button and no other move is being done
    // Signal Computer that move was made and let the ai do its job
    Serial.write(MOVE_MADE);
  }
  
  if (Serial.available() > 0) {
    data = Serial.readString(); // read the entire string from the stack and put it inside a variable
    delay(100);                 // wait little hobbit not so fast.... (if no delay strange things happen)
    ctrl = data[0];
    doConversion(data);
    moveRecieved = true;
  };
  
  // we only process the case when we get a new movement from the PC
  if (moveRecieved){
    // switch through crtl to see what actions to take
    switch(ctrl) {
      case '0':
        movePosition(move_begin,pos_coord); // move from the current position to the begin move position
        Serial.println("Moved to begin of move");
        digitalWrite(MAGNET,HIGH);          // turn on magnet
        movePositionPiece(move_end,move_begin);  // make the move with the piece
        Serial.println("Moving piece");
        digitalWrite(MAGNET,LOW);           // turn off the magnet
        delay(1000);                        // wait 1sec for demagnetization
        updateCurrentPosition();
        break;
      case '1':
        movePosition(move_end,pos_coord);    // move to the final position of the move since this piece will go to jail
        digitalWrite(MAGNET,HIGH);
        movePositionPiece(jail_coord,move_end);
        digitalWrite(MAGNET,LOW);
        delay(1000);
        movePosition(move_begin,jail_coord);
        digitalWrite(MAGNET,HIGH);
        movePositionPiece(move_end,move_begin);
        digitalWrite(MAGNET,LOW);
        delay(1000);
        updateCurrentPosition();
        break;
      case '2':
        // turn on LED
        digitalWrite(LED,HIGH);
        moveRecieved = false; // move was processed
        break;
    };
    
    // put moveRecieved back to false since we already processed it
    moveRecieved = false;
  }
}


//====================================================================================================================
// Helper methods go here :
//====================================================================================================================

void disableMotors(){
  // This method will disable all the motors
  // it simply puts the enable pins of both motors to HIGH as they are active in LOW state
  digitalWrite(EN1,HIGH);
  digitalWrite(EN2,HIGH);
}



void doConversion(String movement){
  for(int i=0;i<=1;i++){    
    move_begin[i] = (int) (movement[1 + i]-'0');
    move_end[i] = (int) (movement[3 + i]-'0');
  }
}

void movePosition(int destination[2], int source[2]) {
  int steps_Y=0;
  int steps_X=0;
  double distanceX=0;
  double distanceY=0;
  int dirX=0;
  int dirY=0;
  distanceX = (destination[0]-source[0])*size_square;
  distanceY = (destination[1]-source[1])*size_square;
  //X Movement
  if (distanceX > 0){
    dirX = 1;
    steps_X= distanceX/prec_m;
  } 
  else {
    dirX = 0;
    distanceX=-distanceX;
    steps_X=distanceX/prec_m;
  }
  //Y Movement
  if (distanceY > 0) {
    dirY = 1;
    steps_Y=distanceY/prec_m;
  }
  else {
    dirY = 0;
    distanceY=-distanceY;
    steps_Y=distanceY/prec_m;
  }
  Serial.println(steps_Y);
  Serial.println(steps_X);
  moveMotors(dirX, steps_X, 2);
  moveMotors(dirY, steps_Y, 1);  
}

void movePositionPiece(int destination[2], int source[2]) {
  moveMotors(1,  steps_deviation, 2);
  moveMotors(1,  steps_deviation, 1);
  
  // move the piece
  movePosition(destination, source);
  
  // move back to center of square
  moveMotors(2,  steps_deviation, 2);
  moveMotors(2,  steps_deviation, 1);
}

void moveMotors(int dir, int steps, int motor){
  int a = 0;
  if (motor == 1) { //Y movement
    digitalWrite(EN1, LOW);
    if (dir == 1){
      digitalWrite(DIR1, HIGH);
    }
    else{
      digitalWrite(DIR1, LOW);
    }
    while (a < steps){
      digitalWrite(STP1,HIGH);   
      delay(5);   
      digitalWrite(STP1,LOW);
      delay(5);
      a++;
    }
  }
  else { //motor = 2 = X movement
    digitalWrite(EN2, LOW);
    if (dir == 1){
      digitalWrite(DIR2, LOW);
    }
    else{
      digitalWrite(DIR2, HIGH);
    }
    while (a< steps){
      digitalWrite(STP2,HIGH);   
      delay(5);   
      digitalWrite(STP2,LOW);
      delay(5);
      a++;
    }
  }
  disableMotors();
}

void updateCurrentPosition() {
  pos_coord[0] = move_end[0];
  pos_coord[1] = move_end[1];
}


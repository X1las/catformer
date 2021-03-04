package piss;

import java.util.*;
import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

import jdk.jfr.Timestamp;
import org.junit.jupiter.api.BeforeEach;




class CircleTest {
    
    Circle circle;

    @BeforeEach
    void setUp(){
        circle = new Circle(new Vector(4,2), Math.sqrt(10/Math.PI));
    }

    @Test
    void area(){
        assertEquals(circle.area(), 10);
    }
    
    
}


/*
@Test
void withdrawal() {
   bankAccount.withdrawal(250);
   assertEquals(bankAccount.balance, 250);
}*/

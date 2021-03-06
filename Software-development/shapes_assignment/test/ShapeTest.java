import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class ShapeTest {

    @Test
    void dist() {
        Triangle tri = new Triangle(new Vector(0,0), new Vector(1,0), new Vector(1,1));
        Circle cir = new Circle(new Vector(2,0), 2);
        Rectangle rec = new Rectangle(new Vector(0,0),1, 1);

        assertEquals(tri.dist(rec), 0.24, 0.01);
        assertEquals(cir.dist(tri), 1.37, 0.01);
        assertEquals(rec.dist(cir), 1.58, 0.01);
    }
}
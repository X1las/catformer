import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class VectorTest {
    Vector vec1, vec2;

    @BeforeEach
    void setUp(){
        vec1 = new Vector(2.72, 3.80);
        vec2 = new Vector(5.56, 1.36);
    }

    @Test
    void length() {
        assertEquals(vec1.length(), 4.67, 0.01);
        assertEquals(vec2.length(), 5.72, 0.01);
    }

    @Test
    void add() {
        double[] actual = {vec1.add(vec2).x, vec1.add(vec2).y};
        double[] expected = {8.28, 5.16};
        assertArrayEquals(actual, expected, 0.01);
    }

    @Test
    void sub() {
        double[] actual = {vec1.sub(vec2).x, vec1.sub(vec2).y};
        double[] expected = {-2.84, 2.44};
        assertArrayEquals(actual, expected, 0.01);
    }

    @Test
    void testToString() {
        assertEquals(vec1.toString(), "(2.72,3.8)");
    }
}
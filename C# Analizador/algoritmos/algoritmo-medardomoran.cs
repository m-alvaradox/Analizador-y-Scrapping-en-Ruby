using System;
public class Persona
{
    int edad = 25;
    string nombre = "Carlos";

    public void MostrarInformacion()
    {
        Console.WriteLine("Nombre: " + nombre);
        Console.WriteLine("Edad: " + edad);

        if (edad >= 18)
        {
            Console.WriteLine("Es mayor de edad.");
        }
        else
        {
            Console.WriteLine("Es menor de edad.");
        }
    }

    public bool EsMayorDeEdad()
    {
        if (edad >= 18)
        {
            return true;
        }
        return false;
    }

    public static void Main(string[] args)
    {
        Persona p = new Persona();
        p.MostrarInformacion();

        bool mayor = p.EsMayorDeEdad();
        Console.WriteLine("¿Mayor de edad?: " + mayor);
    }
}
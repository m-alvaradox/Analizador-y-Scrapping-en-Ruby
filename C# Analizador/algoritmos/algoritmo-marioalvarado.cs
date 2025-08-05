using System;
using System.Collections.Generic;
public class Estudiante
{
    string nombre;
    List<float> notas = new List<float>();

    public void addData()
    {
        nombre = "Astrid";
        notas.Add(9.5f);
        notas.Add(6.5f);
    }

    public void MostrarDatos()
    {
        Console.WriteLine("Nombre: " + nombre);

        float promedio = CalcularPromedio();
        Console.WriteLine("Promedio: " + promedio);


        if (promedio >= 6)
        {
            Console.WriteLine("Ha aprobado el curso.");
        }
        else
        {
            Console.WriteLine("No ha aprobado el curso.");
        }
    }

    private float CalcularPromedio()
    {
        float suma = 0;

        foreach (float nota in notas)
        {
            suma += nota;
        }
        return suma / notas.Count;
    }

    public static void Main(string[] args)
    {
        Estudiante estudiante = new Estudiante();
        estudiante.addData();
        estudiante.MostrarDatos();
    }
}
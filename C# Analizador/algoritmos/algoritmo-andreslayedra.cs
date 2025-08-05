using System;
public class Producto
{
    string nombre = "Mouse inalámbrico";
    float precio = 19.99f;
    int stock = 12;

    public void MostrarInfo()
    {
        Console.WriteLine("Producto: " + nombre);
        Console.WriteLine("Precio: $" + precio);
        Console.WriteLine("Stock disponible: " + stock);

        if (stock > 0)
        {
            Console.WriteLine("Producto en inventario.");
        }
        else
        {
            Console.WriteLine("Producto agotado.");
        }

        if (precio >= 15)
        {
            Console.WriteLine("Precio válido para la venta.");
        }
        else
        {
            Console.WriteLine("Precio demasiado bajo, revisar margen de ganancia.");
        }
    }

    public bool DisponibleParaVenta()
    {
        if (stock > 0 && precio >= 15)
        {
            return true;
        }
        return false;
    }

    public enum Categoria
    {
        Electronica,
        Oficina,
        Hogar
    }

    public struct Garantia
    {
        int anios;
        bool incluyeDanios;

    }
}

public class Inventario
{
    public void ClasificarProducto(int codigo)
    {
        switch (codigo)
        {
            case 100:
                Console.WriteLine("Producto clasificado como: Electrónica");
                break;
            case 200:
                Console.WriteLine("Producto clasificado como: Oficina");
                break;
            case 300:
                Console.WriteLine("Producto clasificado como: Hogar");
                break;
            default:
                Console.WriteLine("Código no reconocido.");
                break;
        }
    }

    public void MostrarCiclo()
    {
        for (int i = 1; i <= 3; i++)
        {
            if (i == 2)
            {
                continue;
            }

            Console.WriteLine("Iteración número: " + i);

            if (i == 3)
            {
                break;
            }
        }
    }

    public void MostrarCaracteres()
    {
        char inicial = 'M';
        char final = 'Z';
        Console.WriteLine("Inicial: " + inicial + ", Final: " + final);
    }
}


public class DiagnosticoInventario
{
    public void EjecutarAnalisis()
    {
        float temperaturaAlmacen = 22.5f;
        bool productoActivo = true;
        string fechaRegistro = "2025-06-14";
        int codigoHex = 0x1F4;
        int codigoBin = 0b1010;

        if (productoActivo)
        {
            Console.WriteLine("Diagnóstico: Producto activo registrado el " + fechaRegistro);
            Console.WriteLine("Código Hex: " + codigoHex + ", Binario: " + codigoBin);
            Console.WriteLine("Temperatura del almacén: " + temperaturaAlmacen + "°C");
        }
        else
        {
            Console.WriteLine("Producto inactivo.");
        }
    }

    public void MostrarMensaje()
    {
        Console.WriteLine("Listo para la venta");
    }

}

public class Programa
{
    public static void Main(string[] args)
    {
        Producto p = new Producto();
        p.MostrarInfo();

        bool puedeVenderse = p.DisponibleParaVenta();
        Console.WriteLine("¿Disponible para la venta?: " + puedeVenderse);

        DiagnosticoInventario d = new DiagnosticoInventario();
        d.EjecutarAnalisis();
        d.MostrarMensaje();
    }
}
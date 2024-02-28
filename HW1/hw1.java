public class hw1 {
    public void bob(){
        for(int i=9; i>=1; i--){
            System.out.print(i + " bottles of beer on the wall, ");
            System.out.println(i + " bottles of beer. ");
            System.out.println("Take one down, pass it around,");
        }
        System.out.println("No more bottles of beer on the wall.\n");
    }
    public static void main(String[] args) {
        hw1 a = new hw1();
        System.out.print("Ho va ten : HUNG MINH TUAN");
        System.out.print("\tMSV : 22022210");
        System.out.print("\tClass : K67 - K1");
        System.out.print("\tUsername Github : 8MTi");
        System.out.println("\tEmail : 22022210@vnu.edu.vn");
        a.bob();


    }
}

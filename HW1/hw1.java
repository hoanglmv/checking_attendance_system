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
        System.out.println("\tHo va ten : HUNG MINH TUAN");
        a.bob();
        System.out.println("\tMSV : 22022210");
        a.bob();
        System.out.println("\tClass : K67 - K1");
        a.bob();
        System.out.println("\tUsername Github : 8MTi");
        a.bob();
        System.out.println("\tEmail : 22022210@vnu.edu.vn");
        a.bob();


    }
}

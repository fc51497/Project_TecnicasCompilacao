max:Int (a: Int, b:Int){
    a > b {
        return a;
    }
    return b;
}
pi:Int = 3;
 pub fn aggregate(list: &[i32]) -> Vec<i32> {
    let len = list.len();
    // the size of the result array is not known until runtime
    // using vec is unavoidable
    let mut ret = vec![0; (len >> 1) + (len & 0b0001)];
    //let mut ret = vec![0;(len )];
    let mut j=0;

    
   
    for i in 0..len {
        if i % 2 == 1 {
            ret[i / 2] += list[i];
        } else {
            ret[i / 2] = list[i]  ;
            
        }
    }
    return ret;
}

fn printall(list: &[i32]) {
    print!("[");
    for i in 0..list.len() {
        print!("{}, ", list[i]);
    }
    println!("]");
}

fn main() {
    let test1: [i32; 6] = [1, 2, 3, 4, 5, 6];
    let ret1 = aggregate(&test1);
    printall(&test1);
    printall(&ret1);
    let test2: [i32; 5] = [1, 2, 3, 4, 5];
    let ret2 = aggregate(&test2);
    printall(&test2);
    printall(&ret2);
}


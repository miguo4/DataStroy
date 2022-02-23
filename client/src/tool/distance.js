export const euclidean = function(v1, v2) {
    var total = 0;
    for (var i = 0; i < v1.length; i++) {
       total += Math.pow(v2[i] - v1[i], 2);      
    }
    return Math.sqrt(total);
}

export const manhattan = function(v1, v2) {
   var total = 0;
   for (var i = 0; i < v1.length ; i++) {
      total += Math.abs(v2[i] - v1[i]);      
   }
   return total;
}

export const factSimilarity = function(f1, f2) {
   // 1. fact
   let s1 = f1.type === f2.type ? 1 : 0;

   // 2. measure
   let s2
   let m1 = f1.measure.map(x=>x.field);
   let m2 = f2.measure.map(x=>x.field);
   if (m1.length === 0 && m2.length === 0) {
      s2 = 1 // no measure
   } else {
      let m_intersection = m1.filter(value => m2.includes(value));
      let m_longer = m1.length > m2.length ? m1 : m2;
      s2 = m_intersection.length / m_longer.length;
   }

   // 3. subspace
   let s3
   let subspace1fields = f1.subspace.map(x=>x.field);
   let subspace2fields = f2.subspace.map(x=>x.field);
   if (subspace1fields.length === 0 && subspace2fields.length === 0) {
      s3 = 1 // subspace is whole data
   } else {
      let subspace_intersection = subspace1fields.filter(value => subspace2fields.includes(value));
      let subspace_longer = subspace1fields.length > subspace2fields.length ? subspace1fields : subspace2fields;
      s3 = subspace_intersection.length / subspace_longer.length;
   }

   // 4. groupby
   let s4;
   let g1 = f1.groupby;
   let g2 = f2.groupby;
   if (g1.length === 0 && g2.length === 0) {
      s4 = 1;
   } else {
      let g_intersection = g1.filter(value => g2.includes(value));
      let g_longer = g1.length > g2.length ? g1 : g2;
      s4 = g_intersection.length / g_longer.length;
   }
   
   // 5. focus
   let s5;
   let focus1 = f1.focus.map(x=>x.value);
   let focus2 = f2.focus.map(x=>x.value);
   if (focus1.length === 0 && focus2.length === 0) {
      s5 = 0; // no focus
   } else {
      let focus_intersection = focus1.filter(value => focus2.includes(value))
      let focus_longer = focus1.length > focus2.length ? focus1 : focus2
      s5 = focus_intersection.length / focus_longer.length
   }

   let similarity = 0.2*s1 + 0.2*s2 + 0.2*s3 + 0.2*s4 + 0.2*s5;
   return similarity;
}

export const factDistance = function(f1, f2) {
   return 1 - factSimilarity(f1, f2)
}
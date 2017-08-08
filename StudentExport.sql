SELECT 
    st.*
FROM
    pesp_q3_nayan_desk.student st
        INNER JOIN
    pesp_q3_nayan_desk.school sc on st.school_id = sc.id
        INNER JOIN
    pesp_q3_nayan_desk.upazilla uz ON sc.upazilla_id = uz.id
    where uz.id in (%s)
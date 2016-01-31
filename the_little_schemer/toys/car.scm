(car (quote (a b c)))
;---

(car (quote ((a b c) x y z)))
;---

(car (quote dumpling))
;---

(car (quote ()))
;---

(car (quote (((dumplings)) (and) (pickle) relish)))
;---

(quote (car (quote (((dumplings)) (and) (pickle) relish))))
;---

(car (car (quote (((dumplings)) (and)))))
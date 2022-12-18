window.onload = function () {
    const productList = document.getElementById("products-list");

    const loadBtn = document.getElementById("load-btn");
    const spinnerBox = document.getElementById("spinner-box");
    const emptyBox = document.getElementById("empty-box");
    const loadsBox = document.getElementById("loading-box");
    const productNum = document.getElementById("product-num")
    const mySelect = document.getElementById("mySelect");
    const selectStatus = document.getElementById("select-status");
    //console.log(productNum);



    let visible = 5;
    const handleGetData = (sorted, sortedStatus) => {
        $.ajax({
            type: "GET",
            url: `/supplier-products-list-ajax/`,
            data: {
                "num_products": visible,
                "order_by": mySelect.value,
                'order_by_status': selectStatus.value,
            },
            success: function (response) {
                const data = response.data;
                console.log(data);
                const maxSize = response.max
                emptyBox.classList.add("not-visible")
                spinnerBox.classList.remove("not-visible")
                loadsBox.classList.add("not-visible")
                if (sorted) {
                    productList.innerHTML = ""
                }
                setTimeout(() => {
                    spinnerBox.classList.add("not-visible")
                    loadsBox.classList.remove("not-visible")

                    if (response.products_size > 0) {
                        productNum.innerHTML = `<p>We found <strong class="text-brand">${response.products_size}</strong> items for you!</p>`
                    }
                    else {
                        productNum.innerHTML = ` <p>Show 0 Of 0 Product</p>`
                    }

                    data.map(product => {
                        let discount = ""
                        if (product.PRDDiscountPrice > 0) {
                            discount = `$${product.PRDDiscountPrice}`
                        }
                        if (product.PRDISactive) {
                            productStatus = 'Active'
                            alertStatus = 'alert-success'
                        } else {
                            productStatus = 'Inactive'
                            alertStatus = 'alert-danger'
                        }
                        let text = product.product_name
                        let textSlice = text.slice(0, 39);
                        let d = new Date(product.date);

                        productList.innerHTML += `<div class="listing">
                        <div class="enhanced-table">
                            <div class="table-repsponsive">
                                <table class="table">
                                    <thead>
                                        <tr><th>Sr.No.</th>
                                            <th>Product ID</th>
                                            <th>product Name</th>
                                            <th>Product Price</th>
                                            <th>Image</th>
                                            <th>Active</th>
                                            <th>Product Pieces</th>
                                            <!-- {% if request.user.is_superuser %} -->
                                            <th>Action</th>
                                            <!-- {% endif %} -->
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr>
                                            {% for product in products %}
                                            {% if product.PRDISactive == True %}
                                            <td>{{forloop.counter}}</td>
                                            <td>{{product.id}}</td>
                                            <!-- <td><a href="/view-profile/{{item.profile.slug}}" class="text-info">{{item.username}}</a></td> -->
                                            <td>{{product.product_name}}</td>
                                            <td>{{request.session.currency}}  {{product.PRDPrice}}</td>
                                            <td><img class="card-img-top rounded-circle" src="{{product.product_image.url}}"
                                                alt="Card image cap"></td>
                                            <td>{{product.PRDISactive}}</td>
                                            <td>{{product.pieces}}</td>
                                            <td>
                                                <button class="icon-button" class="dropdown-toggle"
                                                    id="tableActionDropdown" data-toggle="dropdown" aria-haspopup="true"
                                                    aria-expanded="false">
                                                    <i class="fa fa-cog" aria-hidden="true"></i>
                                                </button>
                                                <form action="" method="post">
                                                    {% csrf_token %}
                                                <ul class="dropdown-menu dropdown-list dropdown-menu-right"
                                                    aria-labelledby="tableActionDropdown">
                                                    <li><a href="/edit-product/{{product.PRDSlug}}" class="dropdown-item"><i class="fa fa-edit"></i> Edit</a></li>
                                                     <li><a href="/delete-product/{{product.PRDSlug}}" class="dropdown-item"><i class="fa fa-trash"></i> Delete</a></li>
                                                </ul>
                                                </form>
                                            </td>
                                        </tr>
                                         {% endif %}
                                    {% endfor %}

                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>`

                    })
                    if (maxSize) {

                        loadsBox.classList.add("not-visible")
                        emptyBox.classList.remove("not-visible")
                        emptyBox.innerHTML = `<strong class="current-price text-brand">No More Products !</strong>`
                    }

                }, 500)


            },
            error: function (error) { }
        })

    }
    handleGetData();
    loadBtn.addEventListener("click", () => {

        visible += 5;

        handleGetData(false);

    })
    $('.mySelect').on('change', function () {

        visible = 5;
        handleGetData(true);
    })

    $('.select-status').on('change', function () {

        visible = 5;
        handleGetData(true);
    })




}
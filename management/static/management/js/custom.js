$(document).ready(function () {
  $('.toggle-button').on('click', function(){
    $('.drawer').toggle();
    $('.main-content').toggleClass('main-section')
  })
  
  //Counter
  $(".counter").each(function () {
    $(this)
      .prop("Counter", 0)
      .animate(
        {
          Counter: $(this).text(),
        },
        {
          duration: 4000,
          easing: "swing",
          step: function (now) {
            $(this).text(Math.ceil(now));
          },
        }
      );
  });
  // Color picker sidebar
  $(".color-picker-btn").on("click", function (e) {
    $(".color-picker").addClass("open-sidenav");
    $(".overlay").addClass("show-overlay");
  });
  $(".overlay").on("click", function (e) {
    $(".color-picker").removeClass("open-sidenav");
    $(this).removeClass("show-overlay");
  });
  // Change theme color
  var theme_classes =
    "dark-theme light-theme warning-theme primary-theme danger-theme success-theme info-theme navbar-light navbar-dark bg-dark bg-light bg-transparent bg-primary";
  $(".dark-picker").on("click", function () {
    $(".dashboard").removeClass(theme_classes);
    $(".header-common").removeClass(theme_classes);
    $(".navbar").removeClass(theme_classes);
    $(".dashboard").addClass("dark-theme");
    $(".header-common").addClass("bg-transparent");
    $(".navbar").addClass("navbar-dark");
    $(this).addClass("selected");
  });
  $(".light-picker").on("click", function () {
    $(".dashboard").removeClass(theme_classes);
    $(".header-common").removeClass(theme_classes);
    $(".navbar").removeClass(theme_classes);
    $(".dashboard").addClass("light-theme");
    $(".header-common").addClass("bg-primary");
    $(".navbar").addClass("navbar-light");
    $(this).addClass("selected");
  });
  $(".default-picker").on("click", function () {
    $(".dashboard").removeClass(theme_classes);
    $(".header-common").removeClass(theme_classes);
    $(".dashboard").addClass("default-theme");
    $(".header-common").addClass("bg-primary");
    $(this).addClass("selected");
  });
  $(".primary-picker").on("click", function () {
    $(".dashboard").removeClass(theme_classes);
    $(".header-common").removeClass(theme_classes);
    $(".dashboard").addClass("primary-theme");
    $(".header-common").addClass("bg-primary");
    $(this).addClass("selected");
  });
  $(".warning-picker").on("click", function () {
    $(".dashboard").removeClass(theme_classes);
    $(".header-common").removeClass(theme_classes);
    $(".dashboard").addClass("warning-theme");
    $(".header-common").addClass("bg-warning");
    $(this).addClass("selected");
  });
  $(".success-picker").on("click", function () {
    $(".dashboard").removeClass(theme_classes);
    $(".header-common").removeClass(theme_classes);
    $(".dashboard").addClass("success-theme");
    $(".header-common").addClass("bg-success");
    $(this).addClass("selected");
  });
  $(".indigo-picker").on("click", function () {
    $(".dashboard").removeClass(theme_classes);
    $(".header-common").removeClass(theme_classes);
    $(".dashboard").addClass("indigo-theme");
    $(this).addClass("selected");
  });
  // Bar graph
  var ctx = $("#chart-line");
  $.ajax({
    type: "GET",
    url: `/chart-ajax/`,
    data: {},
    success: function (response) {
      const productCount=response.product_count_list;
      const ordercount=response.order_count_list;
      var myLineChart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
          datasets: [
            {
              data: productCount,
              label: "Product",
              borderColor: "rgb(44, 85, 149)",
              fill: true,
              backgroundColor: "rgb(44, 85, 149)",
            },
            {
              data: ordercount,
              label: "Order",
              borderColor: "rgb(238 238 238)",
              fill: false,
              backgroundColor: "rgb(238 238 238)",
            },
          ],
        },
        options: {
          title: {
            display: false,
            //text: "Sales / Revenue",
          },
        },
      });
    //  pie
      const mdx = document.getElementById('myChart').getContext('2d');
      const myChart = new Chart(mdx, {
          type: 'doughnut',
          data: {
              labels: ['Red', 'Blue', 'Yellow', 'Green', ],
              datasets: [{
                  label: '# of Votes',
                  data: [12, 19, 3, 5],
                  backgroundColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)'
                  ],
                  borderColor: [
                      'rgba(255, 99, 132, 1)',
                      'rgba(54, 162, 235, 1)',
                      'rgba(255, 206, 86, 1)',
                      'rgba(75, 192, 192, 1)'
                  ],
                  borderWidth: 1
              }]
          },
          options: {
              scales: {
                  y: {
                      beginAtZero: true
                  }
              },
              legend: {
                display: false
              },
              cutoutPercentage: 90,
          }
      });
    
      
    },
    error: function (error) { }
});
//   var myLineChart = new Chart(ctx, {
//     type: "bar",
//     data: {
//       labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
//       datasets: [
//         {
//           data: [0, 10, 20, 14, 30, 50, 18, 60, 3, 10, 7, 12],
//           label: "Sales",
//           borderColor: "rgb(44, 85, 149)",
//           fill: true,
//           backgroundColor: "rgb(44, 85, 149)",
//         },
//         {
//           data: [12, 7, 10, 2, 10, 12, 14, 4, 20, 50, 40, 30],
//           label: "Revenue",
//           borderColor: "rgb(238 238 238)",
//           fill: false,
//           backgroundColor: "rgb(238 238 238)",
//         },
//       ],
//     },
//     options: {
//       title: {
//         display: false,
//         //text: "Sales / Revenue",
//       },
//     },
//   });
// //  pie
//   const mdx = document.getElementById('myChart').getContext('2d');
//   const myChart = new Chart(mdx, {
//       type: 'doughnut',
//       data: {
//           labels: ['Red', 'Blue', 'Yellow', 'Green', ],
//           datasets: [{
//               label: '# of Votes',
//               data: [12, 19, 3, 5],
//               backgroundColor: [
//                 'rgba(255, 99, 132, 1)',
//                 'rgba(54, 162, 235, 1)',
//                 'rgba(255, 206, 86, 1)',
//                 'rgba(75, 192, 192, 1)'
//               ],
//               borderColor: [
//                   'rgba(255, 99, 132, 1)',
//                   'rgba(54, 162, 235, 1)',
//                   'rgba(255, 206, 86, 1)',
//                   'rgba(75, 192, 192, 1)'
//               ],
//               borderWidth: 1
//           }]
//       },
//       options: {
//           scales: {
//               y: {
//                   beginAtZero: true
//               }
//           },
//           legend: {
//             display: false
//           },
//           cutoutPercentage: 90,
//       }
//   });

// //   var productDetails = function () {
// //     $('.product-image-slider').slick({
// //         slidesToShow: 1,
// //         slidesToScroll: 1,
// //         arrows: false,
// //         fade: false,
// //         asNavFor: '.slider-nav-thumbnails',
// //     });

// //     $('.slider-nav-thumbnails').slick({
// //         slidesToShow: 4,
// //         slidesToScroll: 1,
// //         asNavFor: '.product-image-slider',
// //         dots: false,
// //         focusOnSelect: true,

// //         prevArrow: '<button type="button" class="slick-prev"><i class="fi-rs-arrow-small-left"></i></button>',
// //         nextArrow: '<button type="button" class="slick-next"><i class="fi-rs-arrow-small-right"></i></button>'
// //     });

// //     // Remove active class from all thumbnail slides
// //     $('.slider-nav-thumbnails .slick-slide').removeClass('slick-active');

// //     // Set active class to first thumbnail slides
// //     $('.slider-nav-thumbnails .slick-slide').eq(0).addClass('slick-active');

// //     // On before slide change match active thumbnail to current slide
// //     $('.product-image-slider').on('beforeChange', function (event, slick, currentSlide, nextSlide) {
// //         var mySlideNumber = nextSlide;
// //         $('.slider-nav-thumbnails .slick-slide').removeClass('slick-active');
// //         $('.slider-nav-thumbnails .slick-slide').eq(mySlideNumber).addClass('slick-active');
// //     });

// //     $('.product-image-slider').on('beforeChange', function (event, slick, currentSlide, nextSlide) {
// //         var img = $(slick.$slides[nextSlide]).find("img");
// //         $('.zoomWindowContainer,.zoomContainer').remove();
// //         $(img).elevateZoom({
// //             zoomType: "inner",
// //             cursor: "crosshair",
// //             zoomWindowFadeIn: 500,
// //             zoomWindowFadeOut: 750
// //         });
// //     });
// //     //Elevate Zoom
// //     if ($(".product-image-slider").length) {
// //         $('.product-image-slider .slick-active img').elevateZoom({
// //             zoomType: "inner",
// //             cursor: "crosshair",
// //             zoomWindowFadeIn: 500,
// //             zoomWindowFadeOut: 750
// //         });
// //     }
// //     //Filter color/Size
// //     $('.list-filter').each(function () {
// //         $(this).find('a').on('click', function (event) {
// //             event.preventDefault();
// //             $(this).parent().siblings().removeClass('active');
// //             $(this).parent().toggleClass('active');
// //             $(this).parents('.attr-detail').find('.current-size').text($(this).text());
// //             $(this).parents('.attr-detail').find('.current-color').text($(this).attr('data-color'));
// //         });
// //     });
// //     //Qty Up-Down
// //     $('.detail-qty').each(function () {
// //         var qtyval = parseInt($(this).find('.qty-val').text(), 10);

// //         var qtyInput = document.getElementById("qty-input")
// //         if (qtyInput) { document.getElementById("qty-input").value = qtyval; }

// //         $('.qty-up').on('click', function (event) {
// //             event.preventDefault();
// //             qtyval = qtyval + 1;
// //             $(this).prev().text(qtyval);
// //             if (qtyInput) { document.getElementById("qty-input").value = qtyval; }

// //         });
// //         $('.qty-down').on('click', function (event) {
// //             event.preventDefault();
// //             qtyval = qtyval - 1;
// //             if (qtyval > 1) {
// //                 $(this).next().text(qtyval);
// //                 if (qtyInput) { document.getElementById("qty-input").value = qtyval; }

// //             } else {
// //                 qtyval = 1;
// //                 $(this).next().text(qtyval);
// //                 if (qtyInput) { document.getElementById("qty-input").value = qtyval; }

// //             }
// //         });
// //     });

// //     $('.dropdown-menu .cart_list').on('click', function (event) {
// //         event.stopPropagation();
// //     });
// // };

// productDetails();


/*Product Details*/
// var productDetails = function () {
//         $('.product-image-slider').slick({
//             slidesToShow: 1,
//             slidesToScroll: 1,
//             arrows: false,
//             fade: false,
//             asNavFor: '.slider-nav-thumbnails',
//         });

//         $('.slider-nav-thumbnails').slick({
//             slidesToShow: 4,
//             slidesToScroll: 1,
//             asNavFor: '.product-image-slider',
//             dots: false,
//             focusOnSelect: true,

//             prevArrow: '<button type="button" class="slick-prev"><i class="fi-rs-arrow-small-left"></i></button>',
//             nextArrow: '<button type="button" class="slick-next"><i class="fi-rs-arrow-small-right"></i></button>'
//         });

//         // Remove active class from all thumbnail slides
//         $('.slider-nav-thumbnails .slick-slide').removeClass('slick-active');

//         // Set active class to first thumbnail slides
//         $('.slider-nav-thumbnails .slick-slide').eq(0).addClass('slick-active');

//         // On before slide change match active thumbnail to current slide
//         $('.product-image-slider').on('beforeChange', function (event, slick, currentSlide, nextSlide) {
//             var mySlideNumber = nextSlide;
//             $('.slider-nav-thumbnails .slick-slide').removeClass('slick-active');
//             $('.slider-nav-thumbnails .slick-slide').eq(mySlideNumber).addClass('slick-active');
//         });

//         $('.product-image-slider').on('beforeChange', function (event, slick, currentSlide, nextSlide) {
//             var img = $(slick.$slides[nextSlide]).find("img");
//             $('.zoomWindowContainer,.zoomContainer').remove();
//             $(img).elevateZoom({
//                 zoomType: "inner",
//                 cursor: "crosshair",
//                 zoomWindowFadeIn: 500,
//                 zoomWindowFadeOut: 750
//             });
//         });
//         //Elevate Zoom
//         if ($(".product-image-slider").length) {
//             $('.product-image-slider .slick-active img').elevateZoom({
//                 zoomType: "inner",
//                 cursor: "crosshair",
//                 zoomWindowFadeIn: 500,
//                 zoomWindowFadeOut: 750
//             });
//         }
//         //Filter color/Size
//         $('.list-filter').each(function () {
//             $(this).find('a').on('click', function (event) {
//                 event.preventDefault();
//                 $(this).parent().siblings().removeClass('active');
//                 $(this).parent().toggleClass('active');
//                 $(this).parents('.attr-detail').find('.current-size').text($(this).text());
//                 $(this).parents('.attr-detail').find('.current-color').text($(this).attr('data-color'));
//             });
//         });
//         //Qty Up-Down
//         $('.detail-qty').each(function () {
//             var qtyval = parseInt($(this).find('.qty-val').text(), 10);

//             var qtyInput = document.getElementById("qty-input")
//             if (qtyInput) { document.getElementById("qty-input").value = qtyval; }

//             $('.qty-up').on('click', function (event) {
//                 event.preventDefault();
//                 qtyval = qtyval + 1;
//                 $(this).prev().text(qtyval);
//                 if (qtyInput) { document.getElementById("qty-input").value = qtyval; }

//             });
//             $('.qty-down').on('click', function (event) {
//                 event.preventDefault();
//                 qtyval = qtyval - 1;
//                 if (qtyval > 1) {
//                     $(this).next().text(qtyval);
//                     if (qtyInput) { document.getElementById("qty-input").value = qtyval; }

//                 } else {
//                     qtyval = 1;
//                     $(this).next().text(qtyval);
//                     if (qtyInput) { document.getElementById("qty-input").value = qtyval; }

//                 }
//             });
//         });

//         $('.dropdown-menu .cart_list').on('click', function (event) {
//             event.stopPropagation();
//         });

//         productDetails();
//     }

// });



    
// $(document).ready(function() {
//   $('#submitSignUp').click(function () {
//     $(this).css('display', 'none')
//     $('#buttonload').css('display', 'inline-block')
//   })
// })

// ----------------------------------------------------------------------------------


// window.onload =  function () {

//   //console.log("jffffff")
//   const superCategory = document.getElementById("super_category");
//   const mainCategory = document.getElementById("main_category");
//   const subCategory = document.getElementById("sub_category");
//   const miniCategory = document.getElementById("mini_category");

//   const handleGetSuperCategories = () => {
//       $.ajax({
//           type: "GET",

//           url: "/supplier-categories-ajax/",

//           success: function (response) {
//               const dataSuperCategory = response.super_category
//               //console.log(dataSuperCategory)

//               superCategory.innerHTML = ""
//               dataSuperCategory.map(super_category => {
//                   //console.log(subspecialization)
//                   superCategory.innerHTML += `<option  value="${super_category.id}">${super_category.name}</option>`
//               })


//           },
//           error: function (error) {
//               console.log(error)
//           },

//       })
//   }

//   const handleGetMainCategories = (value) => {
//       $.ajax({
//           type: "GET",

//           url: "/supplier-categories-ajax/",
//           data: {
//               "super_category_ajax": value,
//           },
//           success: function (response) {
//               const dataMainCategory = response.main_category
//               mainCategory.innerHTML = ""
//               dataMainCategory.map(main_category => {

//                   mainCategory.innerHTML += `<option  value="${main_category.id}">${main_category.name}</option>`
//               })


//           },
//           error: function (error) {
//               console.log(error)
//           },

//       })
//   }

//   const handleGetSubCategories = (value) => {
//       $.ajax({
//           type: "GET",

//           url: "/supplier-categories-ajax/",
//           data: {
//               "main_category_ajax": value,
//           },
//           success: function (response) {
//               const dataSubCategory = response.sub_category
//               //console.log(dataSubCategory)
//               subCategory.innerHTML = ""
//               dataSubCategory.map(sub_category => {

//                   subCategory.innerHTML += `<option  value="${sub_category.id}">${sub_category.name}</option>`
//               })


//           },
//           error: function (error) {
//               console.log(error)
//           },

//       })
//   }

//   const handleGetMiniCategories = (value) => {
//       $.ajax({
//           type: "GET",

//           url: "/supplier-categories-ajax/",
//           data: {
//               "sub_category_ajax": value,
//           },
//           success: function (response) {
//               const dataMiniCategory = response.mini_category
//               //console.log(dataMiniCategory)
//               miniCategory.innerHTML = ""
//               dataMiniCategory.map(mini_category => {

//                   miniCategory.innerHTML += `<option  value="${mini_category.id}">${mini_category.name}</option>`
//               })


//           },
//           error: function (error) {
//               console.log(error)
//           },

//       })
//   }


//   setTimeout(() => {
//       handleGetMainCategories(superCategory.value);
//   }, 400)
  
//   setTimeout(() => {
//       let mainSelected = document.getElementById("main_category");
//       handleGetSubCategories(mainSelected.value);
//   }, 1000)
  
//   setTimeout(() => {
//       let subSleceted = document.getElementById("sub_category");
//       handleGetMiniCategories(subSleceted.value);
//   }, 1900)


//   $('.super_category').on('change', function () {

//       const superCategoryValue = $(this).val();
//       handleGetMainCategories(superCategoryValue);
//       setTimeout(() => {
//           let mainSelected = document.getElementById("main_category");
//           handleGetSubCategories(mainSelected.value);
//       }, 1000)
//       setTimeout(() => {
//           let subSleceted = document.getElementById("sub_category");
//           handleGetMiniCategories(subSleceted.value);
//       }, 1900)

//   })

//   $('.main_category').on('change', function () {
//       const mainCategoryValue = $(this).val();
//       handleGetSubCategories(mainCategoryValue);

//       setTimeout(() => {
//           let subSleceted = document.getElementById("sub_category");
//           handleGetMiniCategories(subSleceted.value);
//       }, 1000)

//   })

//   $('.sub_category').on('change', function () {
//       const subCategoryValue = $(this).val();
//       setTimeout(() => {
//           handleGetMiniCategories(subCategoryValue);
//       }, 1000)

//   })
// }

// // -------------------------------------------------------

// window.onload = function () {
//   const productList = document.getElementById("products-list");

//   const loadBtn = document.getElementById("load-btn");
//   const spinnerBox = document.getElementById("spinner-box");
//   const emptyBox = document.getElementById("empty-box");
//   const loadsBox = document.getElementById("loading-box");
//   const productNum = document.getElementById("product-num")
//   const mySelect = document.getElementById("mySelect");
//   const selectStatus = document.getElementById("select-status");
//   //console.log(productNum);



//   let visible = 5;
//   const handleGetData = (sorted, sortedStatus) => {
//       $.ajax({
//           type: "GET",
//           url: `/supplier-products-list-ajax/`,
//           data: {
//               "num_products": visible,
//               "order_by": mySelect.value,
//               'order_by_status': selectStatus.value,
//           },
//           success: function (response) {
//               const data = response.data;
//               console.log(data);
//               const maxSize = response.max
//               emptyBox.classList.add("not-visible")
//               spinnerBox.classList.remove("not-visible")
//               loadsBox.classList.add("not-visible")
//               if (sorted) {
//                   productList.innerHTML = ""
//               }
//               setTimeout(() => {
//                   spinnerBox.classList.add("not-visible")
//                   loadsBox.classList.remove("not-visible")

//                   if (response.products_size > 0) {
//                       productNum.innerHTML = `<p>We found <strong class="text-brand">${response.products_size}</strong> items for you!</p>`
//                   }
//                   else {
//                       productNum.innerHTML = ` <p>Show 0 Of 0 Product</p>`
//                   }

//                   data.map(product => {
//                       let discount = ""
//                       if (product.PRDDiscountPrice > 0) {
//                           discount = `$${product.PRDDiscountPrice}`
//                       }
//                       if (product.PRDISactive) {
//                           productStatus = 'Active'
//                           alertStatus = 'alert-success'
//                       } else {
//                           productStatus = 'Inactive'
//                           alertStatus = 'alert-danger'
//                       }
//                       let text = product.product_name
//                       let textSlice = text.slice(0, 39);
//                       let d = new Date(product.date);

//                       productList.innerHTML += `<article class="itemlist mb-3 border-bottom pb-3">
//                       <div class="row align-items-center">
                         
//                           <div class="col-lg-4 col-sm-4 col-8 flex-grow-1 col-name">
//                               <a class="itemside d-flex align-items-center" href="/product-details/${product.PRDSlug}">
//                                   <div class="left mr-3">
//                                       <img src="/media/${product.product_image}" width="100" height="100"   style="width:100px;height:100px;"  class="img-sm img-thumbnail" alt="${product.product_name}" />
//                                   </div>
//                                   <div class="info">
//                                       <h6 class="mb-0">${textSlice}</h6>
//                                   </div>
//                               </a>
//                           </div>
//                           <div class="col-lg-2 col-sm-2 col-4 col-price"><span>$${product.PRDPrice}</span></div>
//                           <div class="col-lg-2 col-sm-2 col-4 col-status">
//                               <span class="badge rounded-pill ${alertStatus}" style="white-space:nowrap">${productStatus}</span>
//                           </div>
//                           <div class="col-lg-1 col-sm-2 col-4 col-date">
//                               <span>${d.toDateString()}</span>
//                           </div>
//                           <div class="col-lg-2 col-sm-2 col-4 col-action text-end">
//                               <a href="/supplier-edit-product/${product.id}/" class="btn btn-primary font-sm rounded btn-brand"> <i class="material-icons md-edit"></i> Edit </a>
//                               <a href="/supplier-products/remove-product/${product.id}/" class="btn btn-danger font-sm btn-danger rounded"> <i class="material-icons md-delete_forever"></i> Delete </a>
//                           </div>
//                       </div>
//                       <!-- row .// -->
//                   </article>`

//                   })
//                   if (maxSize) {

//                       loadsBox.classList.add("not-visible")
//                       emptyBox.classList.remove("not-visible")
//                       emptyBox.innerHTML = `<strong class="current-price text-brand">No More Products !</strong>`
//                   }

//               }, 500)


//           },
//           error: function (error) { }
//       })

//   }
//   handleGetData();
//   loadBtn.addEventListener("click", () => {

//       visible += 5;

//       handleGetData(false);

//   })
//   $('.mySelect').on('change', function () {

//       visible = 5;
//       handleGetData(true);
//   })

//   $('.select-status').on('change', function () {

//       visible = 5;
//       handleGetData(true);
//   })




// }
});
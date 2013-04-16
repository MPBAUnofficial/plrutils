=========
PLR-Utils
=========

A simple PLR helper.

Quick start
-----------

1. Add "plrutils" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'plrutils',
      )

2. Include the plrutils URLconf in your project urls.py like this::

      url(r'', include(plrutils.urls.urlpatterns)),

3. Run `python manage.py syncdb` to create the models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create the database and the functions (you'll need the Admin app enabled).

5. Enjoy.

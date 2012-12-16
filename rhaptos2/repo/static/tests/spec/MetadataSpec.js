// Generated by CoffeeScript 1.3.3
(function() {

  define(['jasmine', 'app/views', 'spec/routes'], function(jasmine, Views, MOCK_CONTENT) {
    var j;
    j = jasmine.getEnv();
    return j.describe('View :: Metadata', function() {
      j.beforeEach(function() {
        this.model = new Views.Module();
        this.model.set(MOCK_CONTENT);
        this.metadataView = new Views.MetadataEditView({
          model: this.model
        });
        this.rolesView = new Views.RolesEditView({
          model: this.model
        });
        this.metadataModal = new Views.ModalWrapper(this.metadataView, 'Edit Metadata (test)');
        return this.rolesModal = new Views.ModalWrapper(this.rolesView, 'Edit Roles (test)');
      });
      return j.describe('(Sanity Check) All Views', function() {
        j.it('should have a .$el', function() {
          expect(this.metadataView.$el).not.toBeFalsy();
          expect(this.rolesView.$el).not.toBeFalsy();
          expect(this.metadataModal.$el).not.toBeFalsy();
          return expect(this.rolesModal.$el).not.toBeFalsy();
        });
        j.it('should initially be hidden', function() {
          return expect(this.metadataView.$el.is(':visible')).toEqual(false);
        });
        return j.it('should show without errors', function() {
          expect(this.metadataModal.show.bind(this.metadataModal)).not.toThrow();
          expect(this.metadataModal.hide.bind(this.metadataModal)).not.toThrow();
          expect(this.rolesModal.show.bind(this.rolesModal)).not.toThrow();
          return expect(this.rolesModal.hide.bind(this.rolesModal)).not.toThrow();
        });
      });
    });
  });

}).call(this);